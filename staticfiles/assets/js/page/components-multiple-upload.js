"use strict";
let dropzones=document.getElementsByName("dropzone");
console.log(dropzones);

for (var dropzone of dropzones){
  var dropzone = new Dropzone(dropzone, {
    url: "#"
  });
  
  var minSteps = 6,
    maxSteps = 60,
    timeBetweenSteps = 100,
    bytesPerStep = 100000;
  
  dropzone.uploadFiles = function(files) {
    var self = this;
  
    for (var i = 0; i < files.length; i++) {
  
      var file = files[i];
        let totalSteps = Math.round(Math.min(maxSteps, Math.max(minSteps, file.size / bytesPerStep)));
  
      for (var step = 0; step < totalSteps; step++) {
        var duration = timeBetweenSteps * (step + 1);
        setTimeout(function(file, totalSteps, step) {
          return function() {
            file.upload = {
              progress: 100 * (step + 1) / totalSteps,
              total: file.size,
              bytesSent: (step + 1) * file.size / totalSteps
            };
  
            self.emit('uploadprogress', file, file.upload.progress, file.upload.bytesSent);
            if (file.upload.progress == 100) {
              file.status = Dropzone.SUCCESS;
              self.emit("success", file, 'success', null);
              self.emit("complete", file);
              self.processQueue();
            }
          };
        }(file, totalSteps, step), duration);
      }
    }
  }
}
// var dropzone = new Dropzone(".mydropzone[1]", {
//   url: "#"
// });

// var minSteps = 6,
//   maxSteps = 60,
//   timeBetweenSteps = 100,
//   bytesPerStep = 100000;

// dropzone.uploadFiles = function(files) {
//   var self = this;

//   for (var i = 0; i < files.length; i++) {

//     var file = files[i];
//       totalSteps = Math.round(Math.min(maxSteps, Math.max(minSteps, file.size / bytesPerStep)));

//     for (var step = 0; step < totalSteps; step++) {
//       var duration = timeBetweenSteps * (step + 1);
//       setTimeout(function(file, totalSteps, step) {
//         return function() {
//           file.upload = {
//             progress: 100 * (step + 1) / totalSteps,
//             total: file.size,
//             bytesSent: (step + 1) * file.size / totalSteps
//           };

//           self.emit('uploadprogress', file, file.upload.progress, file.upload.bytesSent);
//           if (file.upload.progress == 100) {
//             file.status = Dropzone.SUCCESS;
//             self.emit("success", file, 'success', null);
//             self.emit("complete", file);
//             self.processQueue();
//           }
//         };
//       }(file, totalSteps, step), duration);
//     }
//   }
// }