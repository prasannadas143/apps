
serviceapp.controller("ServiceCtl",['$scope', 'fileUpload',
    function($scope) {
        $scope.method = 'POST';
        $scope.url = '/services/addservice/';

        $scope.servicedata = { service_name: "",
                        service_desc: "",
                        service_img: "",
                        price: "",
                        length: "",
                        before: "",
                        after: "",
                        total: "",
                        is_active: "",
                        emp_service: ""
                        };
        $scope.uploadFile = function(){
               file = $scope.myFile;

               console.log('file is ' );
               console.dir(file);

        };


        $scope.submitForm = function() {
            alert(JSON.stringify($scope.servicedata ));
            $scope.uploadFile = function(){
             var file = $scope.service_img;
             fileUpload.uploadFileToUrl(file, url,$scope.servicedata);
        };
     };
  }]);
