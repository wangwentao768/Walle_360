#!/bin/bash
originFile="./originApk/originApk.apk"
zipalignFile="./originApk/zipalignApk.apk"
keyStoreFile="./keystore/apk.keystore"
signCheckJar="./support/CheckAndroidV2Signature.jar"
walleJar="./support/walle-cli-all.jar"

checkSuppot(){
	cd `dirname $0`
	echo "当前路径:" `pwd`
	echo "检测目标文件..."
    if [[ -e ${originFile} ]]; then
    	echo "文件正常"
	    doZipAlign
    else
	    echo "目标文件不存在，请将360加固过的文件放在当前文件夹下，并修改名称为originApk.apk"
    fi
}

doZipAlign(){
	echo "代码对齐优化..."
	./support/zipalign -v 4 ${originFile} ${zipalignFile} > /dev/null
    if [ $? -ne 0 ];then
	    echo "优化失败"
	    sleep 5
	else
		echo "优化完成"
		doSign
    fi
}

doSign(){
	echo "签名..."
	./support/apksigner sign --ks ${keyStoreFile} ${zipalignFile}
    if [ $? -ne 0 ];then
	    echo "签名失败"
	    sleep 5
	else
		echo "签名成功"
		checkSign
    fi
}

checkSign(){
	echo "校验签名..."
	java -jar ${signCheckJar} 
    if [ $? -ne 0 ];then
	    echo "校验签名失败"
	    sleep 5
	else
		echo "校验签名成功"
		putChannel
    fi
}

putChannel(){
	echo "渠道写入..."
	echo "请输入渠道名称"
	finalDir="./finalDir"
	if [[ ! -e ${finalDir} ]]; then
		mkdir finalDir
	fi
	read channelName
	java -jar ${walleJar} put -c "${channelName}" ${zipalignFile} "./${finalDir}/${channelName}$(date +%Y%m%d%h%m%s).apk"
	if [ $? -ne 0 ];then
	    echo "渠道写入失败"
	    sleep 10
	else
		echo ${channelName} "渠道写入成功"
		rm -rf ${zipalignFile}
		sleep 10
		echo "bye~"
    fi
}

checkSuppot

