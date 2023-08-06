from py_clubhouse import Clubhouse

token = "5fa1349d-7850-418b-9659-b0401e2073b4"
cc = Clubhouse(token)
s = cc.search_stories("state:Production")
print(s)
# print(s.update({"description": "test test test"}))
# print(cc.workflows())
# # workflow_id = None
# ch_ids = []
# for story in cc.search_stories():
#     ch_ids.append(story.get("story_id"))
