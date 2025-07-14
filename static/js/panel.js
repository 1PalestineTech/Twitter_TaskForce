const API_BASE_URL = window.location.origin;
const selectedValues = new Set();
function update_input(element){
  
    element.value = Array.from(selectedValues).join(",");
}

async function add_profile(){

    page = document.createElement("div")
    page.id="page"
    page.classList.add("page")
    var html=`<div class="main_form">
    <div style="display:flex;flex-direction:row;justify-content:space-between;"><span>Add Profile</span><span onclick=close_page()><i class="fa-solid fa-x"></i></span></div>
    <hr>
    <div>
    <label for="profile_name">Profile :</label>
    <input type = "text" id ="profile_name">
    </div>
    <div>
    <label for="profile_name">Actions :</label>
    </div>
    <div>
    <select id="tags">
    <option selected Disabled>Select</option>
    `;
      
        fetch(`${API_BASE_URL}/tasks`, {
        method: "GET",
        headers: {
        'Content-Type': 'application/json'
    }   ,
        credentials: 'include'
    })
    .then(response => response.json())
    .then(result => {
    let tasks= result["data"]
    
    if (tasks.length !== 0){
    for (const task of tasks) {
        
        html += `<option value="${task[0]}">${task[1]}</option>`
    }       

}
html+=`</select><input type = "hidden" class="tags_values"></div><div> <button id="btn_profile" class = "green-btn" style="align-self:center;" onclick="manage_profile('add')"> Add Profile </button></div>
    
</div>`

    page.innerHTML=html;
    document.body.appendChild(page)
    select = document.getElementById("tags")
    selectedTags = document.createElement("div")
    selectedTags.className ="selected-tags"
    const hiddenInput =document.querySelector(".tags_values")
select.parentElement.after(selectedTags);


select.onchange = ()=>{
const selectedOption = select.options[select.selectedIndex];
    const value = selectedOption.value;
    
    if (value && !selectedValues.has(value)) {
      selectedValues.add(value);

      const tag = document.createElement('span');
      tag.className = 'tag';
      tag.textContent = selectedOption.textContent;

      const remove = document.createElement('span');
      remove.className = 'remove';
      remove.textContent = '×';
      remove.onclick = () => {
        tag.remove();
        selectedValues.delete(value);
        update_input(hiddenInput);
      };
      update_input(hiddenInput);
      tag.appendChild(remove);
      selectedTags.appendChild(tag);
      select.selectedIndex = 0;
    }
}
})

    
    

   
}
function manage_profile(action,id="",username=""){
    if (action=="add"){
        let profile = document.getElementById("profile_name").value;
        let tasks = document.querySelector(".tags_values").value;
       fetch("/add_profile", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({profile:profile,tasks:tasks}),
    }).then(response =>response.json())
    .then(result => {
        if(result["success"]){
            close_page();
        }else{
            alert("Error Occured")
        }
        

        }
    );
    }else if (action=="edit"){
       add_profile().then(()=>{
        setTimeout(() => {
            let input = document.querySelector("#profile_name");
        input.value = username;
        input.disabled = true;
        hidden = document.createElement("input");
        hidden.type = "hidden";
        hidden.id = "profile_id"
        hidden.value = id;
        input.parentElement.after(hidden)
        document.querySelector("#btn_profile").onclick=edit_profile;
        document.querySelector("#btn_profile").textContent="Edit"
        }, 500);
        

       })
        
    }else if(action == "remove"){
         fetch("/remove_profile", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({profile_id:id}),
    }).then(response =>response.json())
    .then(result => {
        if(result["success"]){
           
            document.querySelector(`.profile_${id}`).remove()
        }else{
            alert("Error Occured")
        }
        

        }
    );

    }

}
function edit_profile(){
    let profile_id = document.querySelector("#profile_id").value;
    let tasks = document.querySelector(".tags_values").value;
     fetch("/edit_profile", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({profile_id :profile_id ,tasks:tasks}),
    }).then(response =>response.json())
    .then(result => {
        if(result["success"]){
            close_page();
        }else{
            alert("Error Occured")
        }
        

        }
    );
}
function manage_user(action,agent_id){
     fetch("/manage_user", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({agent_id:agent_id ,action:action}),
    }).then(response =>response.json())
    .then(result => {
        if(result["success"]){
            if (action =="verify" || action == "reject"){
                document.querySelector(`.verify_${agent_id}`).remove()
            }
            
        }else{
            alert("Error Occured")
        }
        

        }
    );
    if (action =="ban" || action=="unban"){
        let status = document.querySelector(`.status_${agent_id}`)
        if(action =="ban"){
            status.textContent = `Status: Banned`;
            document.querySelector(`.btn_${agent_id}`).innerHTML=`<button class="green-btn" onclick="manage_user('unban','${agent_id}')">Unban</button>`
        }else{
            status.textContent = `Status: Verified`;
            document.querySelector(`.btn_${agent_id}`).innerHTML=`<button class="red-btn" onclick="manage_user('ban','${agent_id}')">Ban</button>`
        }
    }

}
function manage_post(action,post_id){
 fetch("/manage_post", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({post_id:post_id ,action:action}),
    }).then(response =>response.json())
    .then(result => {
        if(result["success"]){
                if(action =="verify" || action =="reject" ){
                    document.querySelector(`.post_${post_id}`).remove()
                }
                    

                
            }

        }
    );
    if (action =="accept" || action=="remove"){
        let status = document.querySelector(`.postStatus_${post_id}`)
        if(action =="remove"){
            status.textContent = `Status: rejected`;
           
            document.querySelector(`.btnPost_${post_id}}`).innerHTML=` <button class="green-btn" onclick="manage_post('accept','${post_id}')">Accept</button>`
        }else{
            status.textContent = `Status: verified`;
            document.querySelector(`.btnPost_${post_id}}`).innerHTML=`<button class="red-btn" onclick="manage_post('remove','${post_id}')">Remove</button>`
        }
    }
}
function close_page(){
    document.getElementById("page").remove();
}


