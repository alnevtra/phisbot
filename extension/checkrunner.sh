function check(){
    check=`pgrep php && echo PHP script is running || echo PHP script is NOT running | head -n 1`
    if [[ "${check}" =~ "PHP script is running" ]]; then
        echo "PHP script is running"
    else
        echo "PHP script is NOT running"
    fi
}
check