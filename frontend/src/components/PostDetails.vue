<template>
<div class="container mt-5">
  <h2>
      {{post.title}}
  </h2>
  <div>
    <img v-if="post.id" id="image"
         :src="require('../assets/images/' + `${post.id}` + '.png')"
         :alt="'Image of post ' + `${post.id}`">
  </div>
  <h4 class="mt-3">
    {{post.body}}
  </h4>
  <div v-if="post.user_id === user.id" class="parent">
    <div class="left" style="border: none">
      <router-link :to="{name:'edit', params:{id:post.id}}"
                 class="btn mt-3 icon"
                 style="background-image: url(https://cdn-icons-png.flaticon.com/512/8103/8103693.png);">
      </router-link>
      <p>Update Post</p>
    </div>
    <div class="left" style="border: none">
      <button
        class = "btn mx-3 mt-3 icon"
        style="background-image: url(https://cdn-icons-png.flaticon.com/512/10135/10135725.png);"
        @click="deletePost">
      </button>
      <p>Delete Post</p>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data(){
    return{
      post:{},
      user:this.$store.state.user,
      confirmDelete: null
    }
  },
  props:{
    id:{
      type:[Number, String],
      required:true
    }
  },
  methods: {
    async getPostData(){
      await fetch(`http://localhost:5000/api/userposts/${this.id}`,{
        method:"GET",
        headers:{
          "Content-Type":"application/json",
          "Authentication-Token":this.$store.state.token
        }
      })
          .then(resp => resp.json())
              .then(data => {this.post = data})
              .catch(error => console.log(error))
    },
    deletePost(){
      this.confirmDelete = confirm("Are you sure you want to delete this post? This action is irreversible!")
      if (this.confirmDelete){
        fetch(`http://localhost:5000/api/userposts/${this.id}`,{
        method:"DELETE",
        headers:{
          "Content-Type":"application/json",
          "Authentication-Token":this.$store.state.token
        }
      })
              .then(()=> {
                this.$router.push({
                  name:"profile"
                })
              })
              .catch(error => console.log(error))
      }
    }
  },
  created(){
    if (!(this.user)){
        this.$store.state.user = JSON.parse(localStorage['user'])
        this.$store.state.token = localStorage['token']
        this.user = this.$store.state.user
      }
    this.getPostData()
  }
}
</script>

<style scoped>
.icon {
    width: 75px;
    height: 75px;
    background-repeat: no-repeat;
    background-size: 100% auto;
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
</style>