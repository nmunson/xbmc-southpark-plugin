import urllib,urllib2,re,xbmcplugin,xbmcgui

HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

def ShowSeasons():
	req = urllib2.Request('http://www.xepisodes.com/')
	req.add_header('User-Agent', HEADER)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<a href="(.+?)" title="South Park - Season .+?">(.+?)</a>').findall(link)
	for url,name in match:
		li=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

		
		       
def ShowEpisodes(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<td class=\'tdseason\'>\n<a href=\'(.+?)\'>\n<img  src=\'(.+?)\'.+?\n</a>\n.+?\n-\n<strong><b>\n(.+?)<br />\n</b></strong>').findall(link)
	for url,thumb,name in match:
		li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		li.setInfo( type="Video", infoLabels={ "Title": name } )
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus('http://xepisodes.com/'+url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)


def PlayVideo(url,name):
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<embed src="http\://www.4shared.com//flash/player.swf\?file=(.+?)" width="590" height="430" allowfullscreen="true" allowscriptaccess="always"></embed>').findall(link)
	g_thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=g_thumbnail)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(str(match[0]),liz)
		

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
				
	return param
	
	      
params=get_params()
url=None
name=None
mode=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
	print ""
	ShowSeasons()
       
elif mode==1:
	print ""+url
	ShowEpisodes(url)
	
elif mode==2:
	print ""+url
	PlayVideo(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
