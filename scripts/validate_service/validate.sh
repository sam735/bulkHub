#!/bin/bash
URL_TO_CHECK="http://ec2-13-235-67-223.ap-south-1.compute.amazonaws.com"
CHECK=$(curl -sL -w "%{http_code}\\n" $URL_TO_CHECK -o /dev/null)
if [ $CHECK == "200" ] ; 
then
    exit 0 ;
else
    exit 1 ;
fi
