

wordNum = "3000-55000"
NumPages  = 12
SortBy    = ["revised_at","kudos_count","hits","bookmarks_count"]
SortCol   = 0
Kudos     = ""
Tags = ""
Raiting = ""
searchText = ""
# Tags = "BDSM"
# Raiting = "13" #13 explict


fandom = "One Direction (Band)"
Rel = "Harry+Styles%2FLouis+Tomlinson"

fandom = "Teen Wolf (TV)"
Rel = "Derek+Hale%2FStiles+Stilinski"




url_suf = "&work_search%5Bbookmarks_count%5D=&work_search%5Bcharacter_names%5D=&work_search%5B"\
            "comments_count%5D=&work_search%5Bcomplete%5D=1&work_search%5Bcreator%5D=&work_search%5B"\
            "fandom_names%5D=" + urllib2.quote(fandom) + "&work_search%5B"\
            "freeform_names%5D="+urllib2.quote(Tags)+ "&work_search%5Bhits%5D=&work_search%5B"\
            "kudos_count%5D=" + urllib2.quote(Kudos) + "&work_search%5Blanguage_id%5D=1&"\
            "work_search%5Bquery%5D="+ urllib2.quote(searchText) +"&work_search%5B"\
            "rating_ids%5D="+ urllib2.quote(Raiting) +"&work_search%"\
            "5Brelationship_names%5D=" + Rel + "&work_search%5Brevised_at%5D=&work_search%5Bshow_restricted%5D=false&work_search%5Bsingle_chapter%5D=0&work_search%5B"\
            "sort_column%5D=" + SortBy[SortCol] + "&work_search%5Bsort_direction%5D=&work_search%5Btitle%5D=&work_search%5B" \
            "word_count%5D=" + urllib2.quote(wordNum)


