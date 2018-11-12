$CLASSPATH  << "C:\Git\RubyImplementation"

#http://doc.sikuli.org/javadoc/org/sikuli/script/Screen.html

require 'net/http'
require 'net/https'
require 'uri'
require 'json'
require 'sikulixapi.jar'
require 'rubygems'
require 'java'

java_import 'org.sikuli.script.Button'
java_import 'org.sikuli.script.Screen'
java_import 'org.sikuli.script.ScreenImage'
java_import 'org.sikuli.script.Region'
java_import 'org.sikuli.script.Region'
include Java

$language = 'ENG'
$graphicsDir = 'C:/Git/sikuliroyale/graphics.sikuli/'

$mainRegion = Region.new(0,130,820,1300)
$notficationRegion = Region.new(0,300,120,400)
$giveCards = []
$getCards = []
$filterGiveCards = []
$filterGetCards = []

screen= Screen.new()

def GetButton(name, language=nil)
	return language ? 
	    ($graphicsDir + "B_#{$language}_#{name}.png") :
		($graphicsDir + "B_#{name}.png") 
end

def ClickButton(name, language=nil)
    puts "Clicking button #{GetButton(name)}"
	$mainRegion.click(GetButton(name,language))
	sleep 0.2
end

def GetCard(name)
	return $graphicsDir + 'C_' + name + '.png'
end



$ocrCards = ['Sparky', 'InfernoDragon', 'Miner', 'Ghost']


def HttpGet(url)
	header = {
		'accept' => 'application/json'
	}
	uri = URI.parse(url)

	https = Net::HTTP.new(uri.host,uri.port)
	https.use_ssl = true
	req = Net::HTTP::Get.new(uri.path, header)
	res = https.request(req)

	JSON.parse(res.body)
end

def GetClanList()
	clanList = HttpGet('https://script.google.com/macros/s/AKfycbyBA307eP56Csrm3b9_SjdrMYK3wkXVOszGj7XNzSXFcSvoLxjP/exec')
	puts clanList
end

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

def LookForSpecificTrade(tradeButton)
    giveRegion = Region.new(85, tradeButton.y-30, 200, tradeButton.y+115)
	getRegion = Region.new(330, tradeButton.y-30, 465, tradeButton.y+115)	
	
	$giveCards.each do |card|
		if (giveRegion.exists(GetCard card)) #.similar(0.85)
			puts "***** Giving #{card} ********"
			ClickButton('ScreenCapture')
			sleep 0.2
			break
		else 
			puts "  not giving #{card}"
		end
	end
	
	$getCards.each do |card|
		if (getRegion.exists(GetCard card)) #.similar(0.85)
			puts "***** Getting #{card} ********"
			ClickButton('ScreenCapture')
			sleep 0.2
			break
		else 
			puts "  not getting #{card}"
		end
	end

	if ($filterGiveCards.count > 0 || $filterGetCards.count > 0)
		filtered = false
		
		$filterGiveCards.each do |card|
			if (giveRegion.exists(GetCard card)) 
				puts "***** filtered give #{card} ********"
				filtered = true
				break
		    else
				puts "  filtering give #{card}"
			end
		end

		break if filtered
		
		$filterGetCards.each do |card|
			if (getRegion.exists(GetCard card)) 
				puts "***** filtered get #{card} ********"
				filtered = true
				break
		    else
				puts "  filtering get #{card}"
			end
		end
		
		if (!filtered)
			ClickButton('ScreenCapture')
			sleep 2
		end
	end
end

def LeaveClan()
	puts "Leaving clan"
	ClickButton('PurpleTrophy')
	ClickButton('Leave', $language)
	ClickButton('Yes', $language)
	sleep 0.5
end

def JoinClan(clanList=nil)
	allClans = $mainRegion.findAll(GetButton('YellowTrophy'))
	$mainRegion.click(allClans.to_a.sample)
	sleep 0.4
	
	if ($mainRegion.exists(GetButton('Join', $language)))
		ClickButton('Join', $language) 
    else # Clan is full
		ClickButton('Close') 
		JoinClan()
		return
	end
	
	if($mainRegion.exists(GetButton('Bottom')))
		ClickButton('Bottom')
		sleep 0.8
	end	
end

def FindTrade()
	if ($mainRegion.exists(GetButton('Trade', $language)))
		trades = $mainRegion.findAll(GetButton('Trade', $language))
		trades.each do |trade|
			puts "Trade button found at #{trade.x}, #{trade.y}"
			($giveCards.any? || $getCards.any? || $filterGetCards.any?) ? LookForSpecificTrade(trade) : TranslateTrade(trade) 
		end
	end 
end

def Scout()	
	FindTrade()

	loop do 
		notificationFound = $notficationRegion.exists(GetButton('Notification2'))
		break unless notificationFound
		$notficationRegion.click(GetButton('Notification2'))
		FindTrade()
	end
	puts "Done looking"
end

$language = 'ITL'
#$giveCards = ['LavaHound', 'Sparky', 'Graveyard']
#$getCards = ['BabyDragon', 'GoblinBarrel', 'InfernoTower', 'Fireball', 'Log', 'Miner']  # 'NightWitch', 'LumberJack', 'Prince'
$filterGiveCards = ['ElectroDragon']
$filterGetCards = ['LavaHound', 'Sparky', 'Graveyard', 'InfernoDragon']
 
while 1
	LeaveClan()
	#clanList = GetClanList()
	JoinClan()
	Scout()
end

