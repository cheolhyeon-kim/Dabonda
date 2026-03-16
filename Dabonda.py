import cv2 as cv

channel = 1
max_channel = 50


zoom_level = 5
zoom_box_radius = 30
zoom_box_margin = 10
mouse_xy = [-1,-1,False]

win = "Dabonda"

def get_video_capture(n):
    url = f'rtsp://210.99.70.120:1935/live/cctv{n:03d}.stream'
    cp = cv.VideoCapture(url)
    return cp

def mouse_event_handler(event, x, y, flags, param):
    if event == cv.EVENT_MOUSEMOVE:
        param[0] = x
        param[1] = y
    elif event == cv.EVENT_LBUTTONDOWN:
        param[2] = True
    elif event == cv.EVENT_LBUTTONUP:
        param[2] = False


video = get_video_capture(channel)




if video.isOpened():
    cv.namedWindow(win)
    cv.setMouseCallback(win, mouse_event_handler, mouse_xy)

    width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv.CAP_PROP_FPS)
    if fps <= 0 or fps > 60: 
        fps = 30.0
    wait_msec = int(1000 / fps)
    

    fourcc = cv.VideoWriter_fourcc(*'DIVX')
    out = cv.VideoWriter('output.avi', fourcc, fps, (width, height))
    
    is_recording = False  
    is_paused = False
    negative = False 
    
    while True:
        if not is_paused:    
            valid, frame = video.read()
            if not valid:
                break
                
            if negative:
                frame = 255 - frame
                

        if is_recording:
            record_frame = cv.resize(frame, (width, height))
            out.write(record_frame)
            cv.circle(frame, (width - 30, 30), 10, (0, 0, 255), -1)
            cv.putText(frame, "REC", (width - 80, 35), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        frame2 = frame.copy()
        if mouse_xy[2]:
            if mouse_xy[0] >= zoom_box_radius and mouse_xy[0] < (width - zoom_box_radius) and mouse_xy[1] >= zoom_box_radius and mouse_xy[1] < (height- zoom_box_radius):
                crop = frame[mouse_xy[1]-zoom_box_radius:mouse_xy[1]+zoom_box_radius, mouse_xy[0]-zoom_box_radius:mouse_xy[0]+zoom_box_radius, :]
                zoom_box = cv.resize(crop, None, fx=zoom_level, fy=zoom_level)
                    
                zoom_h, zoom_w = zoom_box.shape[:2]
                if zoom_h + zoom_box_margin < height and zoom_w + zoom_box_margin < width:
                    frame2[zoom_box_margin:zoom_box_margin+zoom_h, zoom_box_margin:zoom_w+zoom_box_margin] = zoom_box
                    cv.rectangle(frame2, (zoom_box_margin, zoom_box_margin), (zoom_box_margin+zoom_w, zoom_box_margin+zoom_h), (0, 0, 255), 2)
        if is_paused:
            cv.putText(frame2, "PAUSE", (1, int(height)), 
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
        cv.putText(frame2, f"CH: {channel:03d}", (10, height-20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv.imshow(win, frame2)
        

        key = cv.waitKeyEx(wait_msec)
        
        if key == 27:
            break
        elif key == ord(' '):
            is_recording = not is_recording
        elif key == ord('p') or key == ord('P'): 
            is_paused = not is_paused
        elif key == ord('n') or key == ord('N'):
            negative = not negative
        elif key == 0x270000:
            channel += 1
            if channel > 50:
                channel = 1
            video.release()
            video = get_video_capture(channel)
            cv.putText(frame, f"{channel}", (int(width), height), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1 )
            print(f"채널 변경: {channel}")
        elif key == 0x250000:
            channel -= 1
            if channel < 1:
                channel = max_channel
            video.release()
            video = get_video_capture(channel)
            print(f"채널 변경: {channel}")
            

            

            
 
    video.release()
    out.release()
    cv.destroyAllWindows()