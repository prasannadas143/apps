
serviceapp.controller("EmployeeCtrl",['$scope', '$http','fileUpload',
    function($scope,$http,fileUpload) {
        $scope.method = 'POST';
        $scope.url = '/services/addemployee/';

        $scope.employeedata = { 
                        emp_name: "",
                        emp_notes: "",
                        email: "",
                        password: "",
                        phone: "",
                        avatar: "",
                        last_login: "",
                        is_subscribed: 0,
                        is_subscribed_sms:0,
                        is_active: 0
        }
     
        $scope.submitForm = function() {
        console.log(JSON.stringify($scope.employeedata ))
            var file = $scope.avatar;
            data = $scope.employeedata;
            url = $scope.url;
            fileUpload.uploadFileToUrl(file, url, data);
            window.location.href = '/services/employeelist/';
        }  

         $scope.CancelForm = function() {
            window.location.href = '/services/employeelist/';
        }  

     }
            
]);
