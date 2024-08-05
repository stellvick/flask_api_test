call nssm.exe install flask_api_test "open.bat"
call nssm.exe set flask_api_test AppStdout "assets\logs\my_flask_app_logs.log"
call nssm.exe set flask_api_test AppStderr "assets\logs\my_flask_app_logs.log"
call nssm set flask_api_test AppRotateFiles 1
call nssm set flask_api_test AppRotateOnline 1
call nssm set flask_api_test AppRotateSeconds 86400
call nssm set flask_api_test AppRotateBytes 1048576
call sc start flask_api_test