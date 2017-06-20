serviceapp.service('fileUpload', ['$http', function ($http) {
        this.uploadFileToUrl = function(file, uploadUrl,data){
           var fd = new FormData();
           fd.append('file', file);
           for(var key in data)
               fd.append(key,data[key])
           $http.post(uploadUrl, fd, {
              transformRequest: angular.identity,
              headers: {'Content-Type': undefined}
           });
        }

 }]);
