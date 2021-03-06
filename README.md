# **Local dev environment compatibility**
이 discord bot program 은 repl.it 에서 코드를 작성하였으며, 코드 내에서 repl.it 의 DB 를 사용하고 있기 때문에 다른 로컬 개발 환경에서 `from replit import db` 을 불러오더라도 로컬 환경에 설정된 DB가 없기 때문에 작동하지 않습니다.

<br>

# **Activate the discord bot on offline**
웹 서버에 대한 담당자 문서
>일단 배포되면 브라우저 탭을 닫은 후에도 서버가 백그라운드에서 계속 실행됩니다. 서버는 마지막 요청 후 1시간까지 깨어 있고 활성 상태를 유지하다 그 후 절전 단계에 들어갑니다.

따라서 웹 서버가 실행 중이더라도 마지막 요청 후 1시간이 지나면 결국 실행이 중지되기 때문에 bot이 계속해서 요청을 받도록 하여 종료되지 않게 해야 합니다.

이것에 대해 repl.it 에서는 계속해서 코드를 실행할 수 있는 유료 요금제를 제공하기도 하지만, 이 코드에서는 봇을 1시간 이상 계속 실행하는 `UptimeRobot` 무료 서비스를 이용했습니다.

지속적인 ping으로 repl.it 의 웹 서버를 5분마다 update 하거나 rollback 설정할 수 있기 때문에 bot은 절대 절전 단계에 들어가지 않고 강제로 종료하기 전까지 계속해서 실행됩니다.

<br>

# **`$del` 미적용 버그** 
`$del` 을 통해 제거한 격려 메세지는 discord bot 이 재시작되어야만 적용됩니다.

DB에 저장된 메세지 리스트가 `$del` 에 의해 업데이트 되어도 실질적인 동작은 프로그램이 reset 되어야 코드에도 적용됩니다.

<br>

# **`encouragements` 출력문 버그**
`$new` 를 통해 생성한 새로운 메세지들만 출력되고 기존의 `starter_encouragements` 내에 저장된 문장들은 출력되지 않는 버그가 있습니다.

기존의 `starter_encouragements` 내에 저장된 문장들은 프로그램이 완전히 정지된 후 다시 시작했을 때에만 반응 문장에 의해 몇 번 출력되다가 이후부터는 `$list` 에 남아있는 `$new` 를 통해 새로 생성한 문장들끼리만 랜덤하고 반복적이게 출력됩니다.