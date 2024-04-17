<template>
  <div class="container mt-5" >
  <div id="search">
    <input style="width: min-content"
           class="form-control"
           type="text"
           placeholder="Search Users"
           v-model="search"><br>

    <select class="form-control form-select"
            v-on:change="changeRoute($event)">
      <option selected>---Click to view Users---</option>
      <option v-if="(filteredSearch).length===0" selected disabled>
        No users found
      </option>
      <option v-for="username in filteredSearch"
              :key="username.id+'foo'"
              :value="username.id">
        @{{username.username}}
      </option>
    </select>
  </div>
  <div v-for="post in posts.slice().reverse()" :key="post.id">
    <div class="container mt-5">
      <hr>
  <h3 style="text-align: left">
    <span v-if="post.user_id === user.id">Post by</span> <router-link v-if="post.user_id === user.id" :to="{name:'profile'}" class="link-style">@{{post.username}}</router-link>
    <br>
    <span v-if="post.user_id !== user.id">Post by</span> <router-link v-if="post.user_id !== user.id" :to="{name:'profileDetails', params:{id:post.user_id}}" class="link-style">@{{post.username}}</router-link>
  </h3>
      <h2> <router-link :to="{name:'postDetails', params:{id:post.id}}" class="link-style">{{post.title}}</router-link></h2>
  <div>
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
      user:this.$store.state.user,
      usernames:[],
      search:""
    }
  },
  methods:{
    getArticles(){
      console.log(this.user);
      console.log(this.posts);
      fetch('http://127.0.0.1:5000/api/posts',{
        method:"GET",
        headers:{
          "Content-Type":"application/json"
        }
      })
          .then(resp => resp.json())
              .then(data => {
                this.posts.push(...data.posts);
                this.usernames.push(...data.usernames);
              })
              .catch(error => console.log(error))
    },
    deleteArticle(obj){
      fetch(`http://localhost:5000/api/userposts/${obj.id}`,{
        method:"DELETE",
        headers:{
          "Content-Type":"application/json"
        }
      })
              .then(()=> {
                window.location.reload()
              })
              .catch(error => console.log(error))
    },
    changeRoute(e){
      if (e.target.value == this.user.id){
        console.log("Navigating to user profile")
        this.$router.push({
          name:"profile"
        })
      }
      else{
        console.log("Navigating to other profiles")

        this.$router.push({
        name:"profileDetails",
        params:{
          id:e.target.value
        }
      })
      }
    }
  },
  computed:{
    filteredSearch(){
      return this.usernames.filter(p =>{
        return p.username.toLowerCase().indexOf(this.search.toLowerCase()) !== -1;
      })
    }
  },
    created(){
      if (!(this.user)){
        this.$store.state.user = JSON.parse(localStorage['user'])
        this.$store.state.token = localStorage['token']
        this.user = this.$store.state.user
      }
      this.getArticles()
    }
}
</script>

<style scoped>
.link-style{
  font-weight: bold;
  color:black;
  text-decoration: none;
}
.link-style:hover{
  color:grey;
  text-decoration: none;
}

#search input{
  position: absolute;
  top:180px;
  left:700px;
  text-align: center;
}
#search select{
  position: absolute;
  top:225px;
  left:701px;
  width: 220px;
  text-align: center;
}
</style>