
serviceapp.controller("ServiceCtl",['$scope', '$http','$compile','fileUpload',
    function($scope,$http,fileUpload) {
        $scope.method = 'POST';
        $scope.url = '/services/getservices/';
        
        var successCallback = function(response) {
            $scope.services = response.data ;
            console.log( $scope.services);
        }

        var errorCallBack = function(response) {
            $scope.error = response.data ;            
        }
         $http({
            method: 'GET',
            url: $scope.url
        }).then(successCallback, errorCallBack);

     
        $scope.submitForm = function() {
            alert(JSON.stringify($scope.servicedata ));
            var file = $scope.service_img;
            data = $scope.servicedata;
            url = $scope.url;
            fileUpload.uploadFileToUrl(file, url, data);
        
      }

            //Declaring the function to load data from database
            $scope.fillEmployeeList = function (employeename) {
                alert("list of employees");
              
                                            
                $http({
                    method: 'GET',
                    url: '/services/listemployeesname/',
                    data: {}
                }).then(function successCallback(response) {
                    alert(JSON.stringify( response   ));

                                                alert("employees list showed");

                    $scope.employeelist = response.data;
                    alert(JSON.stringify( $scope.employeelist));
                    // alert(employeelist.length);
                    // $scope.employeename="";

                    // if (employeelist != null &&  employeelist.length > 0  ){
                    //         alert("employees list");
                    //           for (var i = 0; i <  employeelist.length; i++)
                    //           {
                    //               $scope.employeename += "<label for=" + employeelist[i].name +  ' > <input type="checkbox" name=' + "check" + employeelist[i].id  + ' ng-model=' + "servicedata.check".concat(employeelist[i].id.toString()) +       " value=" + employeelist[i].id + " />" + employeelist[i].name + " </label>";
                                   
                    //          }
                             
                    //         // var templateEl = angular.element($scope.employeename);
                            // //Now compile the template with scope $scope
                            // $compile(templateEl)($scope);
                            // angular.element('#checkboxes').append(templateEL);
                       //Let's say you have element with id 'foo' in which you want to create a button
                    //}

                });
           }
            //Calling the function to load the data on pageload
           // $scope.fillEmployeeList();
    }
]);
