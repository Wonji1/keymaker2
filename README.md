<h1>건아정보기술(주)
  <h2>KeyMaker
    <h3>인식키 관리 솔루션
      <h4>2020-04-06 ~ 2020-06-05
        <h5>js 코드 --> flask --> static --> 
        <h5>html 코드 --> flask --> template -->
          
<h5>배포방법 --> AWS 인스턴스 우분투에 sudo apt install python3-venv 로 venv 다운 --> 
  디렉터리 생성 후 cd -->python3 -m venv 원하는이름 --> source 원하는이름/bin/activate --> 
  git clone https://github.com/Wonji1/KeyMaker2.git --> pip install -r requirements.txt --> 
  sudo apt-get install libzbar0 --> python app.py --> 서버 ip:5000/login 으로 접속
  
<h5> db 설정 --> flask --> config --> config.py --> database 주소, 포트 등 바꾸기
<h5> API 서버 설정 --> flask --> static --> main --> js --> config.js 주소, 포트 등 바꾸기
