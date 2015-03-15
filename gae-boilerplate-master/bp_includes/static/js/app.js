(function() {
  var app = angular.module('easyLaundry', []).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});

  app.config(['$httpProvider', function($httpProvider) {
	$httpProvider.defaults.useXDomain = true;
   	delete $httpProvider.defaults.headers.common['X-Requested-With'];
}])

	app.controller('LaundryItems', function($scope, $http, $timeout){  
		
		$scope.successTextAlert = "Empty content";
		$scope.showSuccessAlert = false;

		$scope.switchBool = function(value) {
		$scope[value] = !$scope[value];
	};  

    //$scope.initialize = function(){	
	// Get All Item Types, Rates and Weights
  	$http.get('_ah/api/laundry_api/v1/items').success(function(data, status, headers, config) { $scope.laundryweights = data.itemlist; }).error(function(data, status, headers, config) {});	
			
	$scope.orders = [{  ordercounter: 0, status:"INIT", items: [] }];
	//Get All Orders
	$http.get('_ah/api/laundry_api/v1/orders').success(function(data, status, headers, config) { $scope.orders = $scope.orders.concat(data.orderlist); }).error(function(data, status, headers, config) {});	
	
	//};
	
//	timeout( function(){ $scope.initialize(); }, 1000);
	
	  $scope.orderid = 0;
	

	
	  $scope.timeoptions = [
	  {timevalue: '00:00'},
	  {timevalue: '00:30'},
	  {timevalue: '01:00'},
	  {timevalue: '01:30'},	  
	  {timevalue: '02:00'},
	  {timevalue: '02:30'},
	  {timevalue: '03:00'},
	  {timevalue: '03:30'},
	  {timevalue: '04:00'},
	  {timevalue: '04:30'},
	  {timevalue: '05:00'},
	  {timevalue: '05:30'},
	  {timevalue: '06:00'},
	  {timevalue: '06:30'},	  
	  {timevalue: '07:00'},
	  {timevalue: '07:30'},
	  {timevalue: '08:00'},
	  {timevalue: '08:30'},
	  {timevalue: '09:00'},
	  {timevalue: '09:30'},
	  {timevalue: '10:00'},
	  {timevalue: '10:30'},
	  {timevalue: '11:00'},
	  {timevalue: '11:30'},
	  {timevalue: '12:00'},
	  {timevalue: '12:30'},
	  {timevalue: '13:00'},
	  {timevalue: '13:30'},
	  {timevalue: '14:00'},
	  {timevalue: '14:30'},	  
	  {timevalue: '15:00'},
	  {timevalue: '15:30'},	  
	  {timevalue: '16:00'},
	  {timevalue: '16:30'},
	  {timevalue: '17:00'},
	  {timevalue: '17:30'},
	  {timevalue: '18:00'},
	  {timevalue: '18:30'},
	  {timevalue: '19:00'},
	  {timevalue: '19:30'},
	  {timevalue: '20:00'},	  
	  {timevalue: '20:30'},
	  {timevalue: '21:00'},	  
	  {timevalue: '21:30'},
	  {timevalue: '22:00'},	  
	  {timevalue: '22:30'},
	  {timevalue: '23:00'},
	  {timevalue: '23:30'}
	  ];
	  /*$scope.orders = [
	  	{
			orderkey: 0,
			date: 'New Order',
			items: [],
			totalweight: 0,
			status: 'new'
		  }
	  ];*/
	  
	  $scope.selectOrder = function(oid){
		$scope.orderid = oid;
	  };
	  
	  $scope.isOrder = function(oid){
		return $scope.orderid === oid;
	  };

	/*	
	 $scope.laundryweights = [
      {
        itemtype: 'Shirt',
        weight: 1.4
	  } 
    ]; */
	

    $scope.neworderItem = function(){
	
        $scope.orders[$scope.orderid].items.push({name:$scope.name.name, weight:$scope.name.weight, itemkey:$scope.name.itemkey, number:$scope.number});
        $scope.name = '';
        $scope.number = '';
		$scope.orders[$scope.orderid].totalweight = 0;
		
		for (i in $scope.orders[$scope.orderid].items){
			$scope.orders[$scope.orderid].totalweight += $scope.orders[$scope.orderid].items[i].weight * $scope.orders[$scope.orderid].items[i].number;
		}
		
    };
	
    $scope.remove=function(item){ 
	
		var index=$scope.orders[$scope.orderid].items.indexOf(item)	  
		$scope.orders[$scope.orderid].items.splice(index,1);     
	  
		$scope.orders[$scope.orderid].totalweight = 0;
		
		for (i in $scope.orders[$scope.orderid].items){
			$scope.orders[$scope.orderid].totalweight += $scope.orders[$scope.orderid].items[i].weight * $scope.orders[$scope.orderid].items[i].number;
		}
	  
    };
	

		

   $scope.placeorder=function(item){	
		
		$scope.orders[0].pickuptime = $scope.orders[0].pudate.concat('T').concat($scope.orders[0].putime.timevalue).concat(':00.000000');
		$scope.orders[0].droptime = $scope.orders[0].dodate.concat('T').concat($scope.orders[0].dotime.timevalue).concat(':00.000000');
				
		$http.post('_ah/api/laundry_api/v1/placeorder', $scope.orders[0]).success(function(data, status, headers, config) { $scope.showSuccessAlert = true; $scope.successTextAlert = "Order Placed"; 
					
			$scope.orders = [{  ordercounter: 0, status:"INIT", items: [] }];
			//Get All Orders
			$http.get('_ah/api/laundry_api/v1/orders').success(function(data, status, headers, config) { $scope.orders = $scope.orders.concat(data.orderlist); }).error(function(data, status, headers, config) {});	
		
		}).error(function(data, status, headers, config) { });
		

    };
	
	
  });  
	
})();