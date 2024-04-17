<template>
<div style="margin-left: -200px">
  <br>
  <div class="parent" v-if="user">
    <div class="left" style="border-top:2px solid black;
                      border-bottom: 2px solid black;
                      border-radius: 25px;
                      margin-right: -150px;
                      margin-bottom: -250px">
    <h2>@{{user.username}}</h2>
    <h4>{{user.name}}</h4>
      <h6>{{user.bio}} <br/><p v-if="user.phone"> Contact :{{user.phone}}</p></h6>
    </div>
  <div class="right">
    <div class="parent"
         style="margin-bottom: -700px">
      <div class="left" style="border-left: none;">
        <h5>
          Posts - {{nposts}}
        </h5>
      </div>
      <div class="left"
           style="border-left:none; border-right: none">
        <h5>
          <router-link class="topLink" v-bind:class="{ disabled: followers===0 }" to="/followers">
            Followers - {{followers}}
          </router-link>
        </h5>
      </div>
      <div class = "left" style="border-right: none;">
        <h5>
          <router-link class="topLink"  v-bind:class="{ disabled: following===0 }" to="/followings">
            Following - {{following}}
          </router-link>
        </h5>
      </div>
    </div>
  </div>
  </div>
  <br>
  <div class="parent">
    <div class="left"
         style="border: none;
         margin-left: 200px;">
      <router-link class="btn icon"
                   to='/create'
                   style="background-image: url(https://cdn-icons-png.flaticon.com/512/875/875068.png);">
      </router-link>&nbsp;
      <p>Add Post</p>
    </div>
    <div class="left" style="border: none">
      <router-link class="btn icon"
                   to='/edit'
                   style="background-image: url(https://cdn-icons-png.flaticon.com/512/942/942799.png);">
      </router-link>
      <p>Edit Profile</p>
    </div>
    <div class="left" style="border: none">
      <router-link class="btn icon"
                   to='/activity'
                   style="background-image: url(https://cdn-icons-png.flaticon.com/512/478/478544.png);">
      </router-link>
      <p>View Activity</p>
    </div>
  </div>
  <div v-if="posts" class="container mt-5">
    <div v-for="post in posts.slice().reverse()" :key="post.date">
      <div>
        <hr>
        <h2>
          <router-link :to="{name:'postDetails', params:{id:post.id}}" class="link-style">{{post.title}}</router-link>
        </h2>
        <div style="width: content-box; height: content-box">
          <img :src="require('../assets/images/' + `${post.id}` + '.png')"
               :alt="'Image of post ' + `${post.id}`">
        </div>
        <h4 class="mt-3">
          {{post.body}}
        </h4>
      </div>
    </div>
  </div>
  <div class="parent">
    <div class="right"
         style="border: none">
      <button
          style = "background-image: url(https://cdn-icons-png.flaticon.com/512/9208/9208320.png)"
            class="btn icon"
            @click="logoutUser">
      </button>
      <p>Logout</p>
    </div>
    <div class="right"
         style="border: none">
      <button
          style = "background-image: url(https://cdn-icons-png.flaticon.com/512/786/786205.png); margin-left: -15px"
            class="btn icon"
            @click="exportCSV">
      </button>
      <p>Export CSV</p>
    </div>
    <div class="right"
         style="border: none">
        <button
            style = "background-image: url(https://cdn-icons-png.flaticon.com/512/1250/1250743.png)"
              class="btn icon"
              @click="deleteUser">
        </button>
      <p>Delete Profile</p>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data(){
    return{
      user: this.$store.state.user,
      posts:[],
      following:0,
      followers:0,
      confirmDelete:null,
      nposts:0
    }
  },
  methods:{
    async getPosts(){
      await fetch(`http://localhost:5000/api/posts/${this.user.id}`,{
        method:"POST",
        headers:{
          "Content-Type":"application/json"
        }
          })
          .then(resp => resp.json())
              .then(data => {
                this.posts.push(...data);
                this.nposts = Object.keys(data).length;
              })
              .catch(error => console.log(error))
    },

    logoutUser(){
      fetch("http://localhost:5000/api/logout", {
        method:"GET",
        headers:{
          "Content-Type":"application/json",
          "Authentication-Token":this.$store.state.token
        }
      })
          .then(response => {
            if (response.ok){
              this.$router.push({
                name:"login"
              });
                  console.log("Logged Out")
                }
            else
                {
                  console.log("Error")
                }
            response.json()
          })
          .then(data => console.log(data))
          .catch(err => console.log(err))
    },

    async deleteUser(){
      this.confirmDelete = confirm("Are you sure you want to delete your account? This action is irreversible!")
      if(this.confirmDelete){
        await fetch("http://localhost:5000/api/user", {
        method:"DELETE",
        headers:{
          "Content-Type":"application/json",
          "Authentication-Token":this.$store.state.token
        }
      })
          .then(resp => resp.json())
          .catch(err => console.log(err))

      await this.$router.push({
          name:"login"
        })
      }
    },

    exportCSV(){
      fetch("http://localhost:5000/api/job", {
        method:"GET",
        headers: {
          "Content-Type":"application/json",
          "Authentication-Token":this.$store.state.token
        }
      })
          .then(resp => resp.json())
          .catch(err => console.log(err));
      alert("Check your email for the requested details!")
    }
  },
  created() {
    if (!(this.user)){
        this.$store.state.user = JSON.parse(localStorage['user'])
        this.$store.state.token = localStorage['token']
        this.user = this.$store.state.user
      }
    this.getPosts();

    fetch(`http://localhost:5000/api/followers/${this.user.id}`, {
        method:"GET",
        headers:{
          "Content-Type":"application/json"
        }
      })
          .then(resp => resp.json())
        .then(data =>{
          this.followers = Object.keys(data).length;
        })
          .catch(err => console.log(err))

    fetch(`http://localhost:5000/api/followings/${this.user.id}`, {
        method:"GET",
        headers:{
          "Content-Type":"application/json"
        }
      })
          .then(resp => resp.json())
        .then(data =>{
          this.following = Object.keys(data).length;
        })
          .catch(err => console.log(err))
  }
}
</script>

<style scoped>
.disabled {
    pointer-events:none;
    text-decoration: none;
 }
.parent {
  margin: 1rem;
  padding: 2rem 2rem;
}
.parent .left{
  display: inline-block;
  padding: 1rem 1rem;
  vertical-align: middle;
  margin-bottom: 20px;
  border-left: 2px solid black;
  border-right: 2px solid black;
}
.parent .right{
  display: inline-block;
  padding: 1rem 1rem;
  vertical-align: middle;
  margin-left: 200px;
}
.topLink{
  text-decoration: none !important;
  color: #2c3e50;
}
.icon {
    width: 75px;
    height: 75px;
    background-repeat: no-repeat;
    background-size: 100% auto;
}
.link-style{
  text-decoration: none !important;
  color: #2c3e50;
}
</style>