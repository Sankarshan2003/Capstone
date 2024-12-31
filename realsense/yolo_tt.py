import torch
import cv2 as cv


print("Img Processing")
model = torch.hub.load(r'E:\University\RAIS\scripts\yolo_img_p\yolov5','custom',path=r"E:\University\RAIS\scripts\yolo_img_p\yolov5\runs\train\exp\weights\last.pt",source='local', force_reload=True)

model.conf = 0.75
dot_coordinates = []


def getmatrix(frame):
    results = model(frame)
    df = results.pandas().xyxy[0]
    xmin = df.iloc[:,0]
    xmax = df.iloc[:,2]
    ymin = df.iloc[:,1]
    ymax = df.iloc[:,3]

    for i in range(len(xmax)):
        bottomright = [int(xmax[i]),int(ymin[i])]
        topleft = [int(xmin[i]),int(ymax[i])]
        
        cX = int((topleft[0] + bottomright[0]) / 2.0)
        cY = int((topleft[1] + bottomright[1]) / 2.0)
    
        center = (cX,cY)
        
        image = cv.circle(frame,(cX,cY), radius=0, color=(0, 0, 255), thickness=5)
        cv.imshow("obj det", image)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
        dot_coordinates.append((cX, cY))
                
    return dot_coordinates

# if __name__ == "__main__