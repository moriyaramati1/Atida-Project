function handleOption() {
     event.preventDefault();

      var vaccination_number = parseInt(document.getElementById("vaccination_number").value);
      var vaccineInputs = document.getElementById("vaccineInputs");
      let vaccine = document.getElementById("vaccine");
      vaccineInputs.innerHTML =""

      for (var i =1; i <= vaccination_number; i++){
          var element = document.createElement('div');
          element.id = "vaccine_"+String(i);
          element.name = "vaccine"

          var inputLabel1 = document.createElement("label");
          inputLabel1.innerHTML = "  יצרן חיסון  " + i + " ";

          var inputLabel2 = document.createElement("label");
          inputLabel2.innerHTML = "  מועד קבלת החיסון  " ;

          var selectList = document.createElement("select");
          selectList.id = "SelectManufacturer";
          selectList.setAttribute("name", "vaccine_"+String(i)+"_manufacturer");
          var array = ["פייזר","מודרנה","אסטרהזניקה ","נובהווקס"];
          for (var j=0; j< array.length; j++){
              var option = document.createElement("option");
              option.value = array[j];
              option.text = array[j];
              selectList.appendChild(option);
          }
          var date_input = document.createElement("input");

          date_input.setAttribute("type", "date");
          date_input.setAttribute("name", "vaccine_"+String(i)+"_date");
          date_input.setAttribute("id","vaccine_"+String(i)+"_date");
          date_input.max = new Date().toISOString().split("T")[0];
          date_input.required = true;
          element.appendChild(inputLabel1);
          element.appendChild(selectList);
          element.appendChild(inputLabel2);
          element.appendChild(date_input);
          vaccineInputs.appendChild(element);
          vaccineInputs.appendChild(document.createElement("br"));

      }
      if (vaccination_number > 0){
            vaccine.classList.add("show-vaccine");
   }
}

positive.max = new Date().toISOString().split("T")[0];


function enableDisableEndDate() {
      var positive = document.getElementById("positive").value;
      var recovery = document.getElementById("recovery");

      if (positive === "") {
        recovery.value = "";
        recovery.disabled = true;
      } else {
        recovery.disabled = false;
        var date = new Date(positive);
        date.setDate(date.getDate() + 5);
        recovery.min = date.toISOString().split("T")[0];
      }
    }
