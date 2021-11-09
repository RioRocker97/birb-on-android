from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
import json,cv2,base64
from yolo_detect import prepareYolo,runYolo,getAvaLabel

app = FastAPI(docs_url=None,redoc_url=None)

@app.get("/")
def main_out():
    out = json.dumps({
        'Event':'Start up',
        'Status':'OK'
    },indent=None)

    return out
@app.post("/birb-in")
async def birb_in(req:Request):
    body = b''
    async for data in req.stream():
        body+= data
    json_req = json.loads(body.decode("UTF-8"))
    #print(json_req)
    with open("./temp/birb_in.jpg","wb+") as birb_in:
        birb_in.write(base64.b64decode(json_req['img']))
    prepareYolo("./birb_model/bird_first_gather.pt")
    img,label = runYolo("./temp/birb_ex2.jpg")
    print(getAvaLabel())
    _,img_buffer = cv2.imencode(".jpg",img)

    out = json.dumps({
        'Event':"Go to birb-out",
        'Status':"OK",
        'Found_Label':str(label),
        'img':str(base64.b64encode(img_buffer))
    },indent=None)

    return out