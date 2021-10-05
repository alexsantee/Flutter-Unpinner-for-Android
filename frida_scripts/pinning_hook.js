function hook_ssl_verify_result(address)
{
  Interceptor.attach(address, {
    onEnter: function(args) {
      console.log("Disabling SSL validation")
    },
    onLeave: function(retval)
    {
      console.log("Retval: " + retval)
      retval.replace(0x1);
    }
  });
}

function disablePinning()
{
var m = Process.findModuleByName("libflutter.so");
// The libflutter signature goes here
var pattern = "55 41 57 41 56 41 55 41 54 53 48 81 ec f8 00 00 00 c6 02 50"
var res = Memory.scan(m.base, m.size, pattern, {
  onMatch: function(address, size){
      console.log('[+] ssl_verify_result found at: ' + address.toString());

      // Add 0x01 if THUMB function in ARM
      hook_ssl_verify_result(address);//.add(0x01));

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
