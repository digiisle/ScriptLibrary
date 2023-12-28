#!/bin/bash
# 1、上传到目标主机；
# 2、赋予执行权限；
# chmod u+x cleanup_script.sh
# 3、执行脚本；
# nohup bash cleanup_script.sh > cleanup_script.log 2>&1 &
# 4、查看执行结果；
# cat cleanup_script.log
#
# 设置Docker容器名称
container_name="main"

# 定义错误处理函数
function handle_error {
    echo "Error: $1" >&2
    exit 1
}

# 检查容器是否正在运行
if ! docker ps -q --filter "name=$container_name" | grep -q .; then
    handle_error "Container $container_name is not running."
else
    echo "Container $container_name is running,cleanup script starts execution."
fi

# 进入Docker容器并执行命令
docker exec -i "$container_name" bash <<EOF
    # 说明
    # 删除目录下的所有文件
    # find ./dirs/ -type f -delete
    # 删除目录下的所有子目录
    # find ./dirs/ -mindepth 1 -maxdepth 1 -type d -exec rm -rf '{}' \;

    # 以下为实际命令
    echo "切换到指定目录/opt/openresty/download/v3"
    cd /opt/openresty/download/v3 || exit 1

    echo "1.删除temp目录下所有文件"
    echo "Deleted files:"
    find ./temp/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./temp/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    

    echo "2.删除engine_360_linux_x86_pks目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_x86_pks/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_x86_pks/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "3.删除engine_360_linux_x86_zyj目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_x86_zyj/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_x86_zyj/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "4.删除engine_360_linux_x64_pks目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_x64_pks/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_x64_pks/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "5.删除engine_360_linux_x64_zyj目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_x64_zyj/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_x64_zyj/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "6.删除engine_360_linux_arm64_zyj目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_arm64_zyj/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_arm64_zyj/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;

    echo "7.删除engine_360_linux_arm64_pks目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_arm64_pks/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_arm64_pks/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;

    echo "8.删除engine_360_linux_client_arm64目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_client_arm64/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_client_arm64/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "9.删除engine_360_linux_client_mips64目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_client_mips64/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_client_mips64/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "10.删除engine_360_linux_mips64_pks目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_mips64_pks/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_mips64_pks/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "11.删除engine_360_linux_mips64_zyj目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_mips64_zyj/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_mips64_zyj/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "12.删除engine_360_linux_server目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_server/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_server/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "13.删除engine_360_linux_sw64目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_sw64/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_sw64/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "14.删除engine_360_linux_sw64_pks目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_sw64_pks/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_sw64_pks/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "15.删除engine_360_linux_sw64_uos目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_sw64_uos/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_sw64_uos/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "16.删除engine_360_linux_sw64_zyj目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_sw64_zyj/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_sw64_zyj/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "17.删除engine_360_linux_arm64目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_arm64/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_arm64/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "18.删除engine_360_linux_arm64_uos目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_arm64_uos/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_arm64_uos/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;

    echo "19.删除engine_360_linux_mips64目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_mips64/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_mips64/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "20.删除engine_360_linux_mips64_uos目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_mips64_uos/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_mips64_uos/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "21.删除engine_360_linux_x86目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_x86/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_x86/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "22.删除engine_360_linux_x86_uos目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_x86_uos/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_x86_uos/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "23.删除engine_360_linux_x64目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_x64/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_x64/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
    echo "24.删除engine_360_linux_x64_uos目录下所有文件"
    echo "Deleted files:"
    find ./engine_360_linux_x64_uos/ -type f -exec echo {} \; -delete
    echo "Deleted directories:"
    find ./engine_360_linux_x64_uos/ -mindepth 1 -maxdepth 1 -type d -exec echo {} \; -exec rm -rf '{}' \;
    
EOF
# Check the exit status of the Docker exec command
if [ $? -eq 0 ]; then
    echo "Cleanup script executed successfully."
else
    handle_error "Cleanup script encountered an error."
fi