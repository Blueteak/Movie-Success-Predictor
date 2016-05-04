import urllib.request
import json
import codecs

def GetStats(movie):
	response = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/search?part=snippet&q="+movie+"&key=AIzaSyDK2ciBIWVj1TtNTEs1MYi9mbUfj4tPArY")
	html = response.read().decode('utf8')
	jsn = json.loads(html)
	stats = QueryStats(jsn["items"][0]["id"]["videoId"])
	print(stats)
	return stats
	
def QueryStats(id):
	response = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/videos?part=statistics&id="+id+"&key=AIzaSyDK2ciBIWVj1TtNTEs1MYi9mbUfj4tPArY")
	html = response.read().decode('utf8')
	jsn = json.loads(html)
	stats = jsn["items"][0]["statistics"]
	return stats
	
def NormalizedValues(stats, budget):
	vcNorm = stat["viewCount"]/budget
	fcNorm = stat["favoriteCount"]/budget
	ccNorm = stat["commentCount"]
	ldRatio = 0
	if(stat["likeCount"] > 0)
		ldRatio = stat["likeCount"]/(stat["likeCount"]+stat["dislikeCount"]
	data = {}
	data["view_count_norm"] = vcNorm
	data["like_dislike_ratio"] = ldRatio
	data["comment_count_norm"] = ccNorm
	data["fave_count_norm"] = fcNorm
	return data
	
##Test run	
GetStats("BatmanBegins")	

## Prints
#
# {
#	'viewCount': '754804', 
#	'favoriteCount': '0', 
#	'commentCount': '455', 
#	'dislikeCount': '49', 
#	'likeCount': '2716'
# }
