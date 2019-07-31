
import os
from bs4 import BeautifulSoup
from operator import itemgetter
from time import strptime,strftime,mktime,gmtime,localtime
import json
from urllib2 import urlopen,Request
import threading




posts= {"ongoing":[] , "upcoming":[]}#py dict
hackerrank_contests = {"urls":[]}

def get_duration(duration):
    days = duration/(60*24)
    duration %= 60*24
    hours = duration/60
    duration %= 60
    minutes = duration
    ans=""
    if days==1: ans+=str(days)+" day "
    elif days!=0: ans+=str(days)+" days "
    if hours!=0:ans+=str(hours)+"h "
    if minutes!=0:ans+=str(minutes)+"m"
    return ans.strip()
    
def fetch_codechef():
    page = urlopen("http://www.codechef.com/contests")
    soup = BeautifulSoup(page,"html.parser")

    statusdiv = soup.findAll("table",attrs = {"class":"dataTable"})
    upcoming_contests = statusdiv[1].findAll("tr")
    if(len(upcoming_contests) <100):
        for upcoming_contest in upcoming_contests[1:]:
            details = upcoming_contest.findAll("td")
            start_time = strptime(details[2].string, "%Y-%m-%d %H:%M:%S")
            end_time = strptime(details[3].string, "%Y-%m-%d %H:%M:%S")
            duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
            posts["upcoming"].append({"Name" :  details[1].string  , "url" : "http://www.codechef.com"+details[1].a["href"] , "StartTime" : strftime("%a, %d %b %Y %H:%M", start_time),"EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Duration":duration ,"Platform":"CODECHEF" })

        ongoing_contests = statusdiv[0].findAll("tr")
        for ongoing_contest in ongoing_contests[1:]:
            details = ongoing_contest.findAll("td")
            end_time = strptime(details[3].string, "%Y-%m-%d %H:%M:%S")
            posts["ongoing"].append({ "Name" :  details[1].string  , "url" : "http://www.codechef.com"+details[1].a["href"] , "EndTime" : strftime("%a, %d %b %Y %H:%M", end_time) ,"Platform":"CODECHEF"})
    else:
        upcoming_contests = statusdiv[0].findAll("tr")
        for upcoming_contest in upcoming_contests[1:]:
            details = upcoming_contest.findAll("td")
            start_time = strptime(details[2].string, "%Y-%m-%d %H:%M:%S")
            end_time = strptime(details[3].string, "%Y-%m-%d %H:%M:%S")
            duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
            posts["upcoming"].append({"Name" :  details[1].string  , "url" : "http://www.codechef.com"+details[1].a["href"] , "StartTime" : strftime("%a, %d %b %Y %H:%M", start_time),"EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Duration":duration ,"Platform":"CODECHEF" })
            
    

def fetch_hackerearth():
    cur_time = localtime()
    ref_date =  strftime("%Y-%m-%d",  localtime(mktime(localtime())   - 432000))
    duplicate_check=[]

    page = urlopen("https://www.hackerearth.com/chrome-extension/events/")
    data = json.load(page)["response"]
    for item in data:
        start_time = strptime(item["start_tz"].strip()[:19], "%Y-%m-%d %H:%M:%S")
        end_time = strptime(item["end_tz"].strip()[:19], "%Y-%m-%d %H:%M:%S")
        duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
        duplicate_check.append(item["title"].strip())
        
        if item["challenge_type"]=='hiring':challenge_type = 'hiring'
        else: challenge_type = 'contest'

        if item["status"].strip()=="UPCOMING":
            posts["upcoming"].append({ "Name" :  item["title"].strip()  , "url" : item["url"].strip() , "StartTime" : strftime("%a, %d %b %Y %H:%M", start_time),"EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Duration":duration,"Platform":"HACKEREARTH","challenge_type": challenge_type  })
        elif item["status"].strip()=="ONGOING":
            posts["ongoing"].append({ "Name" :  item["title"].strip()  , "url" : item["url"].strip() , "EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Platform":"HACKEREARTH","challenge_type": challenge_type  })
            
    

def fetch_codeforces():
    page = urlopen("http://codeforces.com/api/contest.list")
    data = json.load(page)["result"]
    for item in data:
        
        if item["phase"]=="FINISHED": break
        
        start_time = strftime("%a, %d %b %Y %H:%M",gmtime(item["startTimeSeconds"]+19800))
        end_time   = strftime("%a, %d %b %Y %H:%M",gmtime(item["durationSeconds"]+item["startTimeSeconds"]+19800))
        duration = get_duration( item["durationSeconds"]/60 )
        
        if item["phase"].strip()=="BEFORE":  
            posts["upcoming"].append({ "Name" :  item["name"] , "url" : "http://codeforces.com/contest/"+str(item["id"]) , "StartTime" :  start_time,"EndTime" : end_time,"Duration":duration,"Platform":"CODEFORCES"  })
        else:
            posts["ongoing"].append({  "Name" :  item["name"] , "url" : "http://codeforces.com/contest/"+str(item["id"])  , "EndTime"   : end_time  ,"Platform":"CODEFORCES"  })

def fetch_topcoder():
    try:
        page = urlopen("https://clients6.google.com/calendar/v3/calendars/appirio.com_bhga3musitat85mhdrng9035jg@group.calendar.google.com/events?calendarId=appirio.com_bhga3musitat85mhdrng9035jg%40group.calendar.google.com&singleEvents=true&timeZone=Asia%2FCalcutta&maxAttendees=1&maxResults=250&sanitizeHtml=true&timeMin=2016-07-10T00%3A00%3A00-04%3A00&key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs",timeout=15)
        data = json.load(page)["items"]
        cur_time = localtime()
        for item in data:
            if(item["start"].has_key("date")):continue
                
            start_time = strptime(item["start"]["dateTime"][:19], "%Y-%m-%dT%H:%M:%S")
            start_time_indian = strftime("%a, %d %b %Y %H:%M",start_time)
            end_time = strptime(item["end"]["dateTime"][:19], "%Y-%m-%dT%H:%M:%S")
            end_time_indian = strftime("%a, %d %b %Y %H:%M",end_time)

            duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
            name = item["summary"]
            if "SRM" in name and "description" in item: url = "http://community.topcoder.com/tc?module=MatchDetails&rd="+ item["description"][110:115]
            else :            url = "http://tco15.topcoder.com/algorithm/rules/"
                
            if cur_time<start_time:
                posts["upcoming"].append({ "Name" :  name , "url" : url ,"EndTime" : end_time_indian,"Duration":duration, "StartTime" :  start_time_indian,"Platform":"TOPCODER"  })
            elif cur_time>start_time and cur_time<end_time:
                posts["ongoing"].append({ "Name" :  name , "url" : url ,"EndTime" : end_time_indian,"Platform":"TOPCODER"  })
                    
    except Exception, e:
        pass
    
def fetch_hackerrank_general():
    cur_time = str(int(mktime(localtime())*1000))
    page = urlopen("https://www.hackerrank.com/rest/contests/upcoming?offset=0&limit=10&contest_slug=active&_="+cur_time)
    data = json.load(page)["models"]
    for item in data:
        if not item["ended"] and ("https://www.hackerrank.com/"+item["slug"]) not in hackerrank_contests["urls"]:
            start_time = strptime(item["get_starttimeiso"], "%Y-%m-%dT%H:%M:%SZ")
            end_time = strptime(item["get_endtimeiso"], "%Y-%m-%dT%H:%M:%SZ")
            duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
            if not item["started"]:
                hackerrank_contests["urls"].append("https://www.hackerrank.com/"+item["slug"])
                posts["upcoming"].append({ "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"] , "StartTime" :  strftime("%a, %d %b %Y %H:%M", localtime(mktime(start_time)+19800)),"EndTime" : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800)),"Duration":duration,"Platform":"HACKERRANK"  })
            elif   item["started"]:
                hackerrank_contests["urls"].append("https://www.hackerrank.com/"+item["slug"])
                posts["ongoing"].append({  "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"]  , "EndTime"   : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800))  ,"Platform":"HACKERRANK"  })

def fetch_hackerrank_college():
    cur_time = str(int(mktime(localtime())*1000))
    page = urlopen("https://www.hackerrank.com/rest/contests/college?offset=0&limit=50&_="+cur_time)
    data = json.load(page)["models"]
    for item in data:
        if not item["ended"] and ("https://www.hackerrank.com/"+item["slug"]) not in hackerrank_contests["urls"]:
            start_time = strptime(item["get_starttimeiso"], "%Y-%m-%dT%H:%M:%SZ")
            end_time = strptime(item["get_endtimeiso"], "%Y-%m-%dT%H:%M:%SZ")
            duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
            if not item["started"]:
                hackerrank_contests["urls"].append("https://www.hackerrank.com/"+item["slug"])
                posts["upcoming"].append({ "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"] , "StartTime" :  strftime("%a, %d %b %Y %H:%M", localtime(mktime(start_time)+19800)),"EndTime" : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800)),"Duration":duration,"Platform":"HACKERRANK"  })
            elif   item["started"]:
                hackerrank_contests["urls"].append("https://www.hackerrank.com/"+item["slug"])
                posts["ongoing"].append({  "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"]  , "EndTime"   : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800))  ,"Platform":"HACKERRANK"  })


def fetch_hackalist():
    cur_time = str(int(mktime(localtime())*1000))
    cur_month = localtime().tm_mon 
    cur_month_padded = str(cur_month) if cur_month > 9 else "0" + str(cur_month)
    cur_month_name = strftime("%B",localtime())
    cur_year = str(localtime().tm_year)
    
    req = Request("http://www.hackalist.org/api/1.0/"+ cur_year +"/"+ cur_month_padded +".json")
    req.add_header('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0')
    page = urlopen(req)
    
    data = json.load(page)[cur_month_name]
    for item in data:
        start_time = strptime(item["startDate"]+" "+cur_year, "%B %d %Y")
        end_time = strptime(item["endDate"]+" "+cur_year , "%B %d %Y")
        duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
        
        if cur_time < start_time:
            posts["upcoming"].append({ "Name" :  item["title"]+" ["+item["city"]+"]" , "url" : item["url"] , "StartTime" :  strftime("%a, %d %b %Y %H:%M", localtime(mktime(start_time))),"EndTime" : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time))),"Duration":duration,"Platform":"OTHER"  })
        elif   cur_time > start_time and cur_time < end_time:
            posts["ongoing"].append({  "Name" :  item["title"]+" ["+item["city"]+"]" , "url" : item["url"]  , "EndTime"   : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)))  ,"Platform":"OTHER"  })
 
def fetch_coj():
    contest_types = [["upcoming","coming"],["ongoing","running"]]
    posts["upcoming"] = []
    posts["ongoing"] = []
    for each in contest_types:
        pagenum=1
        while(True):
            page = urlopen("http://coj.uci.cu/tables/"+each[1]+".xhtml?page="+str(pagenum))
            soup = BeautifulSoup(page,"html.parser")
            contests_rows  = soup.findAll("tr")
            cur_time=localtime()
            if(contests_rows[2]["class"][0]=="empty"):
                break
            for contests_row in contests_rows[2:len(contests_rows)-1]:
                contests_td = contests_row.findAll("td")
                contest_id = contests_td[0].string.strip()  
                name = contests_td[2].a.string.strip()
                start_time = strptime(contests_td[3].a.string.strip(), "%Y-%m-%d %H:%M:%S")
                end_time = strptime(contests_td[4].a.string.strip(),"%Y-%m-%d %H:%M:%S")
                duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
                posts[each[0]].append({"Name" : name , "url" : "http://coj.uci.cu/contest/contestview.xhtml?cid="+contest_id,"StartTime" : strftime("%a, %d %b %Y %H:%M", start_time),"EndTime" : strftime("%a, %d %b %Y %H:%M",end_time),"Duration":duration ,"Platform":"COJ" })
            pagenum=pagenum+1
            
        
def fetch():


    posts["upcoming"]=[]
    posts["ongoing"]=[]
    hackerrank_contests["urls"] = []
    thread_list = []
    
    thread_list.append( threading.Thread(target=fetch_codeforces) )
    thread_list.append( threading.Thread(target=fetch_topcoder) )
    thread_list.append( threading.Thread(target=fetch_hackerearth) )
    thread_list.append( threading.Thread(target=fetch_codechef) )
    thread_list.append( threading.Thread(target=fetch_hackerrank_general) )
    thread_list.append( threading.Thread(target=fetch_hackerrank_college) )
    thread_list.append( threading.Thread(target=fetch_coj) )
    

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    posts["upcoming"] = sorted(posts["upcoming"], key=lambda k: strptime(k['StartTime'], "%a, %d %b %Y %H:%M"))
    posts["ongoing"] = sorted(posts["ongoing"], key=lambda k: strptime(k['EndTime'], "%a, %d %b %Y %H:%M"))
    posts["timestamp"] = strftime("%a, %d %b %Y %H:%M:%S", localtime())
    


def wr():
    fetch()
    with open('data.json', 'w') as outfile:
        json.dump(posts,outfile)
