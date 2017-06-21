
serviceapp.controller("ServiceCtl",['$scope', '$http','fileUpload',
    function($scope,$http,fileUpload) {
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
        }
     
        $scope.submitForm = function() {
            alert(JSON.stringify($scope.servicedata ));
            var file = $scope.service_img;
            data = $scope.servicedata;
            url = $scope.url;
            fileUpload.uploadFileToUrl(file, url, data);
        
      }

      $scope.EmployeeList = null;
            //Declaring the function to load data from database
            $scope.fillEmployeeList = function () {
                alert("list employees");
                $http({
                    method: 'GET',
                    url: '/services/listemployeesname/',
                    data: {}
                }).then(function successCallback(response) {
                    alert(JSON.stringify( response   ));

                    $scope.EmployeeList = response.data;
                    alert(JSON.stringify( $scope.EmployeeList ));

                });
           }
            //Calling the function to load the data on pageload
           $scope.fillEmployeeList();
    }
]);
