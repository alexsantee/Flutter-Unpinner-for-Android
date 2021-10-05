function disablePinning()
{
var m = Process.findModuleByName("libflutter.so");
// The libflutter signature goes here
var pattern = "55 41 57 41 56 41 55 41 54 53 48 81 ec f8 00 00 00 c6 02 50"
var res = Memory.scan(m.base, m.size, pattern, {
  onMatch: function(address, size){
    console.log('[+] ssl_verify_result found at: ' + address.toString());
    // The patch value goes here
    address.writeByteArray([0x48, 0xc7, 0xc0, 0x01, 0x00, 0x00, 0x00, 0xc3]) // Return 1
    },
  onError: function(reason){
    console.log('[!] There was an error scanning memory');
    },
  onComplete: function()
    {
    console.log("All done")
    }
  });
}

setTimeout(disablePinning, 1000)

// Modified from https://blog.nviso.eu/2019/08/13/intercepting-traffic-from-android-flutter-applications/
