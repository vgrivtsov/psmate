


var app = angular.module('resume_form', ['ui.bootstrap', 'angular.filter',
                                         'typeahead-focus'])


    app.controller('ResumeItems', function($scope, $http) {



    
    //$scope.cvitems = JSON.parse(ucvval); // make object from json string
    
    //console.log($scope.cvitems)

    $scope.items = [];
    //---.put last data from db to input---
    //---for each cv items get data values---
    angular.forEach($scope.cvitems, function(cvitem) {
        $scope.items.push(angular.forEach(cvitem, function(value, key) { {key : value} }));
        
       });


    //---add new cvitems------------------------------
    var newWorkPosNo = $scope.items.length + 1;
    
    $scope.addnewWorkPos = function() {
          
        $scope.items.push({id : newWorkPosNo,                        
                           Quali : []});

        newWorkPosNo++;
        $scope.addworkpos = true;
        
    };
      
    $scope.removeWorkPos = function(item) {
        var index = $scope.items.indexOf(item);
        $scope.addworkpos = false;

        $scope.items.splice(index, 1);
    };

    //---add new quali--------------------------------

    var newQualiNo = 1;
    
    $scope.addnewQuali = function(itemid) {
        
        var QualiNo = $scope.items.find(item => item.id === itemid).Quali.length + newQualiNo
          
        $scope.items.find(item => item.id === itemid).Quali.push({id : QualiNo});
        newQualiNo++;

    };
      
    $scope.removeQuali = function(itemid, quali) {
        var index = $scope.items.find(item => item.id === itemid).Quali.indexOf(quali);

        $scope.items.find(item => item.id === itemid).Quali.splice(index, 1);
    };    
    
    
$scope.getitems = function(){
   
console.log($scope.items)

}

    $scope.selectitems = [
                     {id : "32", name : "Авиастроение" },
                     {id : "31", name : "Автомобилестроение" },
                     {id : "7", name  : "Административно-управленческая и офисная деятельность" }, 
                     {id : "10", name : "Архитектура, проектирование, геодезия, топография и дизайн" },
                     {id : "24", name : "Атомная промышленность" }, 
                     {id : "23", name : "Деревообрабатывающая и целлюлозно-бумажная промышленность, мебельное производство" },
                     {id : "18", name : "Добыча, переработка угля, руд и других полезных ископаемых" }, 
                     {id : "19", name : "Добыча, переработка, транспортировка нефти и газа" }, 
                     {id : "2", name  : "Здравоохранение" }, 
                     {id : "4", name  : "Культура, искусство" }, 
                     {id : "21", name : "Легкая и текстильная промышленность" }, 
                     {id : "14", name : "Лесное хозяйство, охота" }, 
                     {id : "27", name : "Металлургическое производство" }, 
                     {id : "12", name : "Обеспечение безопасности" }, 
                     {id : "1", name  : "Образование и наука" }, 
                     {id : "22", name : "Пищевая промышленность, включая производство напитков и табака" }, 
                     {id : "28", name : "Производство машин и оборудования" }, 
                     {id : "29", name : "Производство электрооборудования, электронного и оптического оборудования" }, 
                     {id : "25", name : "Ракетно-космическая промышленность" }, 
                     {id : "15", name : "Рыбоводство и рыболовство" }, 
                     {id : "6", name  : "Связь, информационные и коммуникационные технологии" }, 
                     {id : "13", name : "Сельское хозяйство" }, 
                     {id : "33", name : "Сервис, оказание услуг населению (торговля, техническое обслуживание, ремонт, предоставление персональных услуг, услуги гостеприимства, общественное питание и пр.)" }, 
                     {id : "40", name : "Сквозные виды профессиональной деятельности" }, 
                     {id : "3", name  : "Социальное обслуживание" }, 
                     {id : "11", name : "Средства массовой информации, издательство и полиграфия" }, 
                     {id : "16", name : "Строительство и жилищно-коммунальное хозяйство" }, 
                     {id : "30", name : "Судостроение" }, 
                     {id : "17", name : "Транспорт" }, 
                     {id : "5", name  : "Физическая культура и спорт" }, 
                     {id : "8", name  : "Финансы и экономика" }, 
                     {id : "26", name : "Химическое, химико-технологическое производство" }, 
                     {id : "20", name : "Электроэнергетика" }, 
                     {id : "9", name  : "Юриспруденция" }, 
                ];    






    //-------------PS----------------------------------  
    $scope.selectps = []; // select PS
    $scope.loadPS = function (selectedOtrasl, itemid, qualiid){
    $http({
      url: '/load_ps',
    	method: 'GET',
    	params: {id: selectedOtrasl}
      
    }).then(function SelectPS(response) {

        $scope.selectps[qualiid] = response.data;
       //console.log(response.data)

       //$scope.items.find(item => item.id === itemid).Quali.find(quali => quali.id === qualiid).FL_cv_PS_target = $scope.PSdata.PurposeKindProfessionalActivity;
       //$scope.items.find(item => item.id === itemid).Quali.find(quali => quali.id === qualiid).FL_cv_OKZ = $scope.PSdata.ListOKZ;
       //$scope.items.find(item => item.id === itemid).Quali.find(quali => quali.id === qualiid).FL_cv_OKVED = $scope.PSdata.ListOKVED;


     
    }, function PSerror(response) {
        $scope.selectps = response.statusText;
    });
    }
    

    //------------Load competence---------------------------
    $scope.selectcompt = []; // select PS
    $scope.loadCompt = function (selectedPS, itemid,qualiid){
    $http({
      url: '/load_compt',
    	method: 'GET',
    	params: {id: selectedPS}
      
    }).then(function SelectCompt(response) {
    
        //$scope.selectcompt[qualiid] = response.data;
        $scope.items.find(item => item.id === itemid).Quali.find(quali => quali.id === qualiid).FL_cv_TF = response.data;

        //
        //$scope.items.find(item => item.id === itemid).Quali.find(quali => quali.id === qualiid).FL_cv_TF = $scope.PSdata.WF_code_name;
        
        //$scope.items.find(item => item.id === itemid).Quali.find(quali => quali.id === qualiid).FL_cv_RS = $scope.PSdata.RequiredSkills;
        //$scope.items.find(item => item.id === itemid).Quali.find(quali => quali.id === qualiid).FL_cv_NK = $scope.PSdata.NecessaryKnowledges;
        //$scope.items.find(item => item.id === itemid).Quali.find(quali => quali.id === qualiid).FL_cv_OC = $scope.PSdata.OtherCharacteristics;        
        
        
        
    }, function Comptterror(response) {
        $scope.selectcompt = response.statusText;
    });
    }

    

});


  
