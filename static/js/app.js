
function loadLikes(){
fetch("/load_data", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({task_name:"Like"}),
    }).then(response =>response.json())
    .then(result => {
        let app = document.querySelector(".app_body");
        app.innerHTML = '';
        div = document.createElement("div")
        div.classList.add("flex-parent")
        div.classList.add("verify-user")
       
        for (post of result["data"]){
            div.innerHTML+=`
            <div class="flex-el like_${post[2]}">
                <div>Post</div>
                <div>Made By: ${post[0]}</div>

                <div>
                <blockquote class="twitter-tweet">
                
                    <a href="https://twitter.com/${post[0]}/status/${post[2]}"></a>
                </blockquote>
                </div>
                <div class="buttons" >
                    <button class="green-btn" onclick="like('${post[2]}')">Like</button>
                </div>
              
            </div>`
            
        }
          
          app.appendChild(div)
          twttr.widgets.load();
        }
    );
}
function loadRetweet(){
    fetch("/load_data", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({task_name:"Retweet"}),
    }).then(response =>response.json())
    .then(result => {
        let app = document.querySelector(".app_body");
        app.innerHTML = '';
        div = document.createElement("div")
        div.classList.add("flex-parent")
        div.classList.add("verify-user")
        for (post of result["data"]){
            div.innerHTML+=`
            <div class="flex-el retweet_${post[2]}">
                <div>Post</div>
                <div>Made By: ${post[0]}</div>

                <blockquote class="twitter-tweet">
  <a href="https://twitter.com/${post[0]}/status/${post[2]}"></a>
</blockquote>
                <div class="buttons" >
                    <button class="green-btn" onclick="retweet('${post[2]}')">Retweet</button>
                </div>
                
            </div>`
            
        }
          app.appendChild(div)
twttr.widgets.load();
        }
    );
}

function loadFollow(){
            fetch("/load_data", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({task_name:"Follow"}),
    }).then(response =>response.json())
    .then(result => {
    
         let app = document.querySelector(".app_body");
        app.innerHTML = "";
        div = document.createElement("div")
        div.classList.add("flex-parent")
        div.classList.add("verify-user")
        for (user of result["data"]){
            div.innerHTML +=`<div class="flex-el follow_${ user[0]}">
                <div>Follow Profile</div>
                <div>Username: ${ user[1] }</div>
                <div>Profile: <a href="https://www.x.com/${ user[1] }">${ user[1] }</a></div>
                <div class="buttons">
                <button class="green-btn" onclick="follow('${ user[0]}')">Follow</button>
                </div>
            </div>`
        }
          app.appendChild(div)
twttr.widgets.load();
        }
    );
}
function loadMute(){
                fetch("/load_data", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({task_name:"Mute"}),
    }).then(response =>response.json())
    .then(result => {
         let app = document.querySelector(".app_body");
        app.innerHTML = "";
        div = document.createElement("div")
        div.classList.add("flex-parent")
        div.classList.add("verify-user")
       
             
        for (user of result["data"]){
            div.innerHTML +=`<div class="flex-el mute_${ user[0]}">
                <div>Mute Profile</div>
                <div>Username: ${ user[1] }</div>
                <div>Profile: <a href="https://www.x.com/${ user[1] }">${ user[1] }</a></div>
                <div class="buttons">
                <button class="green-btn" onclick="mute('${ user[0]}')">Mute</button>
                </div>
            </div>`
        }
        
        
          app.appendChild(div)

        }
    );
}
function loadTweet(){
    document.querySelector(".app_body").innerHTML=`
     <textarea  id="tweet"></textarea>
    <div>
    <button class="green-btn" onclick="tweet()">Tweet</button>
    </div>`;
}

function loadComments(){
fetch("/load_data", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({task_name:"Like"}),
    }).then(response =>response.json())
    .then(result => {
        let app = document.querySelector(".app_body");
        app.innerHTML = '';
        div = document.createElement("div")
        div.classList.add("flex-parent")
        div.classList.add("verify-user")
        
        for (post of result["data"]){
            div.innerHTML+=`
            <div class="flex-el comment_${post[2]}">
                <div>Post</div>
                <div>Made By: ${post[0]}</div>

                
                <blockquote class="twitter-tweet">
                <a href="https://twitter.com/${post[0]}/status/${post[2]}"></a>
                </blockquote>
                
                <div class="buttons" >
                    <button class="green-btn" onclick="commentForm('${post[2]}')">Comment</button>
                </div>
            </div>`
            
        }
          app.appendChild(div)
          twttr.widgets.load();

        }
    );
}

function commentForm(tweet_id){

    page = document.createElement("div")
    page.id="page"
    page.classList.add("page")
    var html=`<div class="main_form">
    <div style="display:flex;flex-direction:row;justify-content:space-between;"><span>Comment Tweet</span><span onclick=close_page()><i class="fa-solid fa-x"></i></span></div>
    <hr>
    <div>
        <label for="comment_data">Comment :</label><br>
        <textarea id ="comment_data">
        </textarea>
    </div>
        <div>
        <button class ="green-btn" onclick="comment(${tweet_id})">Comment</button>
        </div>
    </div>
   
    `;

    page.innerHTML=html;
    document.body.appendChild(page)
}

/*

                                              ACTIONS

*/

function comment(tweet_id){
    text = document.querySelector("#comment_data").value;
    fetch("/comment", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({tweet_id:tweet_id,text:text}),
    }).then(response =>response.json())
    .then(result => {
       
        if (result["status"]!=200){
            alert("There is error Try later")

        } else{
            close_page()
            document.querySelector(`.comment_${tweet_id}`).remove()
        }

        }
    );
}




function tweet(){
    textarea = document.querySelector("#tweet");
    text = textarea.value
    fetch("/tweet", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({tweet:text}),
    }).then(response =>response.json())
    .then(result => {
       
        if (result["status"]!=200){
            alert("There is error Try later")

        } else{
            alert("Tweet Posted")

            textarea.value = ""
        }

        }
    );
}
function follow(id){
    fetch("/follow", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({profile_id:id}),
    }).then(response =>response.json())
    .then(result => {
       
        if (result["status"]!=200){
            alert("There is error Try later")

        } else{
            document.querySelector(`.follow_${id}`).remove()
        }

        }
    );

}
function mute(id){
    fetch("/mute", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({profile_id:id}),
    }).then(response =>response.json())
    .then(result => {
      
        if (result["status"]!=200){
            alert("There is error Try later")

        } else{
            document.querySelector(`.mute_${id}`).remove()
        }

        }
    );

}
function retweet(tweet_id){
fetch("/retweet", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({tweet_id:tweet_id}),
    }).then(response =>response.json())
    .then(result => {
       
        if (result["status"]!=200){
            alert("There is error Try later")

        } else{
            document.querySelector(`.retweet_${tweet_id}`).remove()
        }

        }
    );
}
function like(tweet_id){
fetch("/like", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({tweet_id:tweet_id}),
    }).then(response =>response.json())
    .then(result => {
       
        if (result["status"]!=200){
            alert("There is error Try later")

        } else{
            document.querySelector(`.like_${tweet_id}`).remove()
        }

        }
    );
}