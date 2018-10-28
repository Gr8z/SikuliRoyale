$CLASSPATH  << "C:\Git\RubyImplementation"

#http://doc.sikuli.org/javadoc/org/sikuli/script/Screen.html

require 'sikulixapi.jar'
require 'rubygems'
require 'java'

java_import 'org.sikuli.script.Button'
java_import 'org.sikuli.script.Screen'
java_import 'org.sikuli.script.ScreenImage'
java_import 'org.sikuli.script.Region'
java_import 'org.sikuli.script.Region'
include Java

$graphicsDir = 'C:/Git/RubyImplementation/graphics.sikuli/'

$mainRegion = Region.new(0,60,670,1200)
$notficationRegion = Region.new(0,250,100,330)
$TargetCards = []
$TargetCardsTradeCounter = 0

screen= Screen.new()

def GetButton(name)
	return $graphicsDir + 'B_' + name + '.png'
end

def GetCard(name)
	return $graphicsDir + 'C_' + name + '.png'
end

def ClickButton(name, region=nil)
    puts "Clicking button #{GetButton(name)}"
	region ? region.click(GetButton name) : $mainRegion.click(GetButton name)
	sleep 0.2
end

$ocrCards = ['Sparky', 'InfernoDragon', 'Miner', 'Ghost']

def TranslateTrade(tradeButton)
    puts "Found a trade at #{tradeButton.x}, #{tradeButton.y}" 
	
	giveRegion = Region.new(0, tradeButton.y-30, 200, tradeButton.y+100)  
	getRegion = Region.new(270, tradeButton.y-30, 400, tradeButton.y+100)	
	
	giveCard, getCard = nil
		
	$ocrCards.each do |card|
		if (giveRegion.exists(GetCard(card)) && giveCard.nil?)
			giveCard = card
		end
		
		if (getRegion.exists(GetCard(card)) && getCard.nil?)
			getCard = card
		end
	end	
	
	puts "\n[Give] #{giveCard} [Get] #{getCard} *****"
end

def LookForSpecificTrade(tradeButton, cardNames)
	getRegion = Region.new(270, tradeButton.y-30, 400, tradeButton.y+100)	
	
	cardNames.each do |card|
		if (getRegion.exists(GetCard card))
			puts "***** Found #{card} ********"
			ClickButton('ScreenCapture')
			sleep 0.2
			$TargetCardsTradeCounter = $TargetCardsTradeCounter + 1
			break
		else 
			puts "  not #{card}"
		end
	end

end

def LeaveClan()
	puts "Leaving clan"
	ClickButton('PurpleTrophy')
	ClickButton('Leave')
	ClickButton('Yes')
	sleep 0.5
end

def JoinClan(clanList=nil)
	allClans = $mainRegion.findAll(GetButton('YellowTrophy'))
	$mainRegion.click(allClans.to_a.sample)
	sleep 0.2
	if ($mainRegion.exists(GetButton('Join')))
		ClickButton('Join') 
    else # Clan is full
		ClickButton('Close') 
		JoinClan()
		return
	end
	
	sleep 0.5
	ClickButton('Bottom')
	sleep 0.8
end

def FindTrade()
	if ($mainRegion.exists(GetButton('Trade')))
		trades = $mainRegion.findAll(GetButton('Trade'))
		
		trades.each do |trade|
			puts "Trade button found"
			($TargetCards .any?) ? LookForSpecificTrade(trade, $TargetCards) : TranslateTrade(trade) 
		end
	end 
end

def Scout()	
	FindTrade()

	loop do 
		notificationFound = $notficationRegion.exists(GetButton('Notification2'))
		break unless notificationFound
		ClickButton('Notification2', $notficationRegion)
		sleep 0.1
		FindTrade()
	end
	puts "Done looking"
end


$TargetCards = ['Poison', 'GoblinBarrel', 'BabyDragon', 'Prince']
while $TargetCardsTradeCounter < 100
	LeaveClan()
	JoinClan()
	Scout()
end

