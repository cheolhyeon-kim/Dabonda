# Dabonda
Dabonda Recorder is an OpenCV-based real-time CCTV monitoring system featuring video recording and Live area zooming by mouse click

## 주요 기능 
1. 실시간 RTSP 스트리밍: 001번부터 050번까지의 CCTV 채널을 실시간으로 연결합니다.
2. 영상 녹화: 실시간 화면을 DIVX코덱을 이용하여 .avi파일로 저장한다
3. 채널 전환: 방향키를 이용해 간편하게 채널을 넘겨볼 수 있습니다. 
4. Click-to-Zoom: 마우스 왼쪽 버튼을 누르고 있는 동안 해당 지점을 확대해서 볼 수 있습니다. 
5. 화면 효과 및 제어:
     a.Negative Filter: 야간 시야 확보를 위한 반전 효과 지원합니다
     b.Pause:정지화면을 통해 화면을 자세하게 볼 수 있습니다
     c.Click-to-Zoom: 마우스 왼쪽 버튼을 누르고 있는 동안 해당 지점을 확대해서 볼 수 있습니다. 

## 함수 및 로직 설명 
| 함수              | 설명                                                               |
| :--------------------------- | :----------------------------------------------------------------------------- |
| **get_video_capture(n)**     | 채널 번호 `n`을 기반으로 RTSP 주소를 생성하고 `cv.VideoCapture` 객체를 반환하여 네트워크 스트림을 연결합니다.      |
| **mouse_event_handler(...)** | 마우스 좌표를 실시간으로 추적하고, 좌클릭 `Down/Up` 이벤트를 감지하여 클릭 상태 및 확대 기능에 필요한 좌표 정보를 업데이트합니다.|

| 로직 |	설명  |
| :--------------------------- | :----------------------------------------------------------------------------- |
| 프레임 획득 |	is_paused 상태가 아닐 때만 video.read()를 호출하여 새로운 프레임을 가져오고 화면을 갱신합니다.|
| 영상녹화|	is_recording 상태일 때 현재 프레임을 영상 파일에 저장하고 화면에 REC와 빨간색원을 표시합니다.|
| 클릭 확대 |	마우스 좌클릭 상태일 때 NumPy 슬라이싱으로 ROI 영역을 추출하고 cv.resize()를 이용해 5배 확대하여 표시합니다.|
| 색상 반전|	픽셀 연산 (255 - frame)을 적용하여 전체 영상의 색상을 반전시킵니다.|
| 채널 전환|	기존 VideoCapture 객체를 release()한 뒤 방향키 입력에 따라 새로운 채널의 RTSP 스트림에 재접속합니다.|



## 기능설명
| 기능 (Function) | 키 (Key) | 설명 (Description) |
| :--- | :---: | :--- |
| **녹화 토글** | `Space` | 현재 채널의 영상을 실시간으로 기록 및 저장 (`AVI` 형식) |
| **채널 전환** | `←`, `→` | 001~050번 사이의 RTSP 네트워크 스트림 채널을 실시간 순환 |
| **색상 반전**|	  `N`       |전체 영상의 색상을 반전 |
| **일시정지** | `P` | 라이브 피드를 정지하여 정지 화면 분석 지원 (백그라운드 녹화 유지) |
| **영역 확대** | `마우스 좌클릭` | 클릭 상태를 유지하면 해당 좌표를 5배율로 실시간 확대  |
| **종료** | `ESC` | 모든 스트림 연결을 해제하고 프로그램을 안전하게 종료 |

## 🎥 영상 저장 
     압축 코덱 : DIVX  사용
     파일 형식 : .avi 형식으로 저장
     프레임 속도 (FPS): 소스 영상의 속도에 맞춰 30.0 FPS로 고정하여 실제 시간과 동기화된 영상을 기록
     저장 기법: cv.VideoWriter 객체를 통해 실시간으로 처리된 데이터를 프레임 단위로 인코딩하여 파일 시스템에 기록
     녹화 모니터링: 녹화가 진행되는 동안 원본 프레임에 영향을 주지 않는 별도의 레이어를 사용하여 화면에 빨간색 원과 REC 문구를 표시

## Screenshots

<img width="796" height="637" alt="스크린샷 2026-03-17 073737" src="https://github.com/user-attachments/assets/e3f1f7ce-d6cc-4021-b62d-e4b276f7ad34" />
<녹화 진행중>


<img width="791" height="637" alt="스크린샷 2026-03-17 074421" src="https://github.com/user-attachments/assets/30fc805a-2c2e-4230-b15a-9966f90257e4" />
<채널 변경 후(왼쪽 방향키 이용)>


<img width="894" height="635" alt="스크린샷 2026-03-17 073851" src="https://github.com/user-attachments/assets/60e5859c-6204-4c4a-a236-4fb4fcf4b97a" />
<화면정지>


<img width="901" height="635" alt="스크린샷 2026-03-17 073905" src="https://github.com/user-attachments/assets/108cd764-86e5-40f5-b609-5e2c2ca759ac" />
<반전 적용>


<img width="901" height="633" alt="스크린샷 2026-03-17 073939" src="https://github.com/user-attachments/assets/25004779-62c0-4ec5-9b64-847fa27b8cee" />
<영역 확대>


## 실행

```bash
pip install opencv-python
python Dabonda.py
```

## Tech Stack
Language: Python 3.10.0

Library: OpenCV (Open-source Computer Vision Library) 4.13.0

Tools: GitHub
