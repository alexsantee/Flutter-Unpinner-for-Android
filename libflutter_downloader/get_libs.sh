# Directory structure for download

for folder in release profile debug
do
	mkdir $folder
	cd $folder
	for arch in arm arm64 x64
	do
		mkdir $arch
	done
	cd ..
done

mkdir flutter_versions
cd flutter_versions

# Downloads flutter versions in flutter_versions.txt
while read -r line
do
	# Donwload version
	filename=flutter_linux_${line}-stable.tar.xz
	if [ ! -f ${filename} ]
	then
		wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/${filename}
	fi

	# Extract files
	echo "Extraindo arquivo ${filename}"
	tar -xf ${filename}
	cd flutter/bin/cache/artifacts/engine/
	do_engine_exist=$?
	for mode in release profile debug
	do
		if [ $mode == 'release' ]; then
			mode_append='-release'
		fi
		if [ $mode == 'profile' ]; then
			mode_append='-profile'
		fi
		if [ $mode == 'debug' ]; then
			mode_append=''
		fi

		for arch in arm arm64 x64
		do
			if [ $arch == 'arm' ]; then
				arch_folder='armeabi-v7a'
			fi
			if [ $arch == 'arm64' ]; then
				arch_folder='arm64-v8a'
			fi
			if [ $arch == 'x64' ]; then
				arch_folder='x86_64'
			fi

			jar -xf ./android-${arch}${mode_append}/flutter.jar
			mv ./lib/${arch_folder}/libflutter.so ../../../../../../${mode}/${arch}/libflutter-${line}.so
			rm -r lib
		done
	done
	if [ $do_engine_exist -eq 0 ]; then # for some flutter releases, libflutter is not at the same place, which was breaking the script
		cd ../../../../../ # exits flutter
	fi

	rm -r flutter # Deletes unused extracted files
done < ../flutter_versions.txt

cd .. # exits flutter_versions
