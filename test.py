import re

# String: "web.image.tag=1.0.4"
# becomes
# dict: { "web": { "image": { "tag": "1.0.4"}}}
def string_to_dict(value):
    out = {}
    k,v = value.split("=")
    if re.search(r'\.', k):
        temp = k.split('.')
        temp.append(v)
        out = reduce(lambda x,y: {y: x}, temp[::-1])
    else:
        out[k] = v
    print out

set_string = "web.image.tag=1.0.4"

# string_to_dict(set_string)
string_to_dict(set_string)
string_to_dict("this=something")
