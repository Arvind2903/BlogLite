<template>
<div id="following">
  <h2>You are Following</h2>
  <div v-for="following in followings" :key="following.id">
    <router-link :to="{name:'profileDetails', params:{id:following.following_id}}">
      <h3>@{{following.username}}</h3>
    </router-link>
  </div>
</div>
</template>

<script>
export default {
  data(){
    return{
      user:this.$store.state.user,
      followings:[]
    }
  },
  methods:{
    getFollowings(){
      if (!(this.user)){
        this.$store.state.user = JSON.parse(localStorage['user'])
        this.$store.state.token = localStorage['token']
        this.user = this.$store.state.user
      }
      fetch(`http://localhost:5000/api/followings/${this.user.id}`, {
        method:"GET",
        headers:{
          "Content-Type":"application/json"
        }
      })
          .then(resp => resp.json())
        .then(data =>{
          this.followings.push(...data)
        })
          .catch(err=>console.log(err))
    }
  },
  created(){
    this.getFollowings()
  }
}
</script>

<style scoped>
#following{
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