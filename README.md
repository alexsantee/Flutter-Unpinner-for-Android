# Flutter Unpinner for Android

This is a simple Python script to bypass the x.509 certificate check in Flutter apps in Android.
It is useful if you want to analyze the application through a proxy during a Pentest, since Flutter ignores the system certificates (and proxy). This behavior of using it's own certificates is similar to applications that do certificate pinning, hence this program name.

The method this script use is Flutter version dependent and was tested with many versions, but it is not guaranteed to work right away. If it does not work with your libflutter version, it may be necessary to find it's signature by hand and add it to the signature list, YMMV. Please do a pull request with this new signature if you find it.

This unpinning method is mostly based on [this](https://blog.nviso.eu/2019/08/13/intercepting-traffic-from-android-flutter-applications/) and [this](https://raphaeldenipotti.medium.com/bypassing-ssl-pinning-on-android-flutter-apps-with-ghidra-77b6e86b9476) works.

## How does it work

The certificate checking of Flutter is done in the `ssl_crypto_x509_session_verify_cert_chain` function at the `ssl_x509.cc` file in Google's boringssl. The function returns false if the certificate is invalid and true if it is valid.

What this script does is simply find the function in the binary using a list of known signatures in the `signatures` folder and overwrites it with code that just returns true from the `patches` folder.

These "signatures" are the first bytes of known compilations of the checker function.
At the `signatures` folder there is also `.full` files with all the bytes of the functions, witch are trimmed for the normal signature file, if there are too little bytes there are many false positives and if there are too many it works in fewer libflutter versions.

## Usage

* Get the `libflutter.so` file from the app, witch can be done through `adb pull` or extracting it from the apk
* Run it through the `patcher.py` script (`python3 patcher.py [<input_file> [<output_file>]]`)
* Overwrite the old libflutter with `adb push` and restart the app
* Profit!

Instead of overwriting the libflutter with the patched one, it is also possible to modify the certificate checking function behavior at runtime with Frida. There are scripts for hooking and patching the function at the folder `frida_scripts`, but is necessary to edit the `pattern` variable with the signature found in your libflutter and (for the patch script) edit the writeByteArray function with the patch for your architecture at the `patches` folder.

## Libflutter downloader

To get a good coverage of libflutters it was necessary to extract the libflutter from many Flutter releases. The script used to download these distributions from [here](https://flutter.dev/docs/development/tools/sdk/releases) and extract their `libflutter.so` is in the `libflutter_downloader` folder.
If you want to download this libflutter collection be aware that just the stable channel Flutter releases sum up to dozens of GBs.

## TODO

The armv8 patch is currently untested and there is not many signatures for it. I was unable to get a armv8 phone or armv8 emulator to work on these.

The armv7 may not work if the certificate checker function is not in thumb mode. Further checking is necessary to see if this is an issue.

## Other resources for Flutter pentesting

* [darter](https://github.com/mildsunrise/darter)
* [doldrums](https://github.com/rscloura/Doldrums)
* [flutter binary format](https://rloura.wordpress.com/2020/12/04/reversing-flutter-for-android-wip/)
* [flutter reversing guide](https://blog.tst.sh/reverse-engineering-flutter-apps-part-1/)
