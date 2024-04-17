<template>
<div>
  <h2>View your 24 hour activities</h2>
  <label :for="selected">Choose what activity to view: &nbsp;</label>
  <select v-model="selected" >
    <option value="logins">logins</option>
    <option value="posts">posts</option>
    <option value="follows">follows</option>
    <option value="unfollows">unfollows</option>
  </select>
  <img v-if="selected"
      :src="require('../assets/graphs/'+`${selected}`+'.png')"
      :alt="'login activity'"><hr>
</div>
</template>

<script>
export default {
  data(){
    return{
      selected:null
    }
  },

  methods:{
    getActivity(){
      if (!(this.$store.state.token)){
        this.$store.state.user = JSON.parse(localStorage['user'])
        this.$store.state.token = localStorage['token']
      }
      fetch('http://localhost:5000/api/activity', {
        method:"GET",
        headers:{
          "Content-Type":"application/json",
          "Authentication-Token":this.$store.state.token
        }
      })
          .then(resp => resp.json())
          .then(data => {
            console.log(data);
          })
          .catch(err => console.log(err))
    }
  },
  created() {
    this.getActivity()
  }
}
</script>

<style scoped>

</style>