<template>
<div id="followers">
  <h2>You are followed by</h2>
  <div v-for="follower in followers" :key="follower.id">
    <router-link :to="{name:'profileDetails', params:{id:follower.follower_id}}">
      <h3>@{{follower.username}}</h3>
    </router-link>
  </div>
</div>
</template>

<script>
export default {
  data(){
    return{
      user:this.$store.state.user,
      followers:[]
    }
  },
  methods:{
    getFollowers(){
      if (!(this.user)){
        this.$store.state.user = JSON.parse(localStorage['user'])
        this.$store.state.token = localStorage['token']
        this.user = this.$store.state.user
      }
      fetch(`http://localhost:5000/api/followers/${this.user.id}`, {
        method:"GET",
        headers:{
          "Content-Type":"application/json"
        }
      })
          .then(resp => resp.json())
        .then(data =>{
          this.followers.push(...data)
        })
          .catch(err=>console.log(err))
    }
  },
  created(){
    this.getFollowers()
  }
}
</script>

<style scoped>
#followers{
  position: absolute;
    top: 35%;
    left: 22%;
    margin-top: -50px;
    margin-left: -50px;
    width: 1000px;
    height: 100px;
}
a{
  color: #2c3e50;
}
</style>