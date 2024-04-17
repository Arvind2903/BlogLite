<template>
<div style="margin-left: -50px">
  <div class="parent" v-if="user">
    <div class="left" style="border-top:2px solid black; border-bottom: 2px solid black; border-radius: 25px; margin-right: -150px; margin-bottom: 110px" >
    <h2>@{{user.username}}</h2>
    <h4>{{user.name}}</h4>
    <h6>Bio: {{user.bio}} <br/> Phone :{{user.phone}}</h6>
    </div>
    <div class="right">
    <div  class="parent" v-if="isFollowing!==null">
      <div class="left" style="border-left: none;">
        <h5>Posts - {{nposts}}</h5><br>
      </div>
      <div class="left"
           style="border-left:none; border-right: none">
        <h5 v-if="followers!==null">Followers - {{followers}}</h5><br>
      </div>
      <div class = "left" style="border-right: none;">
        <h5 v-if="following!==null">Following - {{following}}</h5><br>
      </div>
    </div>
      <div>
    <button
      :class="{'btn unfollow':isFollowing,'btn follow':! isFollowing}"
      @click="updateFollowStatus">
    </button>
        <p>{{this.isFollowing ? 'Unfollow' : 'Follow'}}</p>
  </div>
    </div>
  </div>
  <br>

  <div v-for="post in posts.slice().reverse()" :key="post.id">
    <div class="container mt-5">
      <hr>
      <h2> <router-link :to="{name:'postDetails', params:{id:post.id}}" class="link-style">{{post.title}}</router-link></h2>
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
</template>

<script>
export default {
  data(){
    return{
      posts:[],
      user:null,
      isFollowing:null,
      followers:null,
      following:null,
      nposts:0
    }
  },
  props:{
    id:{
      type:[Number, String],
      required:true
    }
  },
  methods:{
    async getUser(){
      if (!(this.$store.state.token))
          {
            this.$store.state.user = JSON.parse(localStorage['user'])
            this.$store.state.token = localStorage['token']
          }

      await fetch(`http://localhost:5000/api/user/${this.id}`,{
        method:'POST',
        headers:{
          "Content-Type":"application/json"
        }
      })
          .then(resp => resp.json())
          .then(data=>{this.user = data})
          .catch(error => console.log(error))

      fetch(`http://localhost:5000/api/posts/${this.id}`, {
        method:'POST',
        headers:{
          "Content-Type":"application/json"
        }
      })
          .then(resp => resp.json())
          .then(data => {
            this.posts.push(...data);
            this.nposts = Object.keys(data).length;
          })
          .catch(error => console.log(error));

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

      fetch(`http://localhost:5000/api/followers/${this.id}`,{
        method:'POST',
        headers:{
          "Content-Type":"application/json",
          "Authentication-Token":this.$store.state.token
        }
      })
          .then(resp => resp.json())
          .then(data=>{
            console.log(`following: ${data.isFollowing}`);
            this.isFollowing = !!data.isFollowing;
          })
          .catch(error => console.log(error))
    },
    async updateFollowStatus(){
      if (this.isFollowing)
      {
        await fetch(`http://localhost:5000/api/followings/${this.id}`,{
        method:'DELETE',
        headers:{
          "Content-Type":"application/json",
          "Authentication-Token":this.$store.state.token
        }
      })
            .then(resp => resp.json())
            .then(data => console.log(data))
            .catch(err => console.log(err))
        console.log("unfollowed")
      }
      else
      {
        await fetch(`http://localhost:5000/api/followings/${this.id}`,{
        method:'POST',
        headers:{
          "Content-Type":"application/json",
          "Authentication-Token":this.$store.state.token
        }
      })
            .then(resp => resp.json())
            .then(data => console.log(data))
            .catch(err => console.log(err))
        console.log("followed")
      }
      this.isFollowing = ! this.isFollowing
      window.location.reload();
    }
  },
  created(){
    this.getUser()
  }
}
</script>

<style scoped>

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

.follow{
  width: 75px;
  height: 75px;
  background-image: url(https://cdn-icons-png.flaticon.com/512/3683/3683218.png);
  background-size: 100%;
  background-repeat: no-repeat;
}
.unfollow{
  width: 75px;
  height: 75px;
  background-image: url(https://cdn-icons-png.flaticon.com/512/3683/3683211.png);
  background-size: 100%;
  background-repeat: no-repeat;
}
.link-style{
  text-decoration: none !important;
  color: #2c3e50;
}
</style>