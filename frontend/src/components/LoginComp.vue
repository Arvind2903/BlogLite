<template>
<div>
  <br>
  <h2>Sign in to use BlogLite</h2>
  <div class="container card-group mt-4">
    <form @submit.prevent="loginUser">
      <p style="text-align: left">*Email:</p>
      <input
        type="text"
        class="form-control"
        placeholder="Email"
        v-model="email">
      <br/>
      <p style="text-align: left">*Password:</p>
      <input
        type="password"
        class="form-control"
        placeholder="Password"
        v-model="password">
      <br>
      <button
        class="btn"
        style="background-image: url(https://cdn-icons-png.flaticon.com/512/1828/1828391.png);
               background-size: 100%; width: 50px; height: 50px">
      </button>
      <p>Sign In</p>
      <br/>
      <div>Not a current user? <router-link to="/signup" style="text-decoration: none;"><b><h5>Sign up</h5></b></router-link></div>
      <div v-if="error" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
        <strong>{{error}}</strong>
      </div>
    </form>
  </div>
</div>
</template>

<script>
import {mapMutations} from "vuex";

export default {
  data(){
    return{
      email:null,
      password:null,
      error:null
    }
  },
  methods:{
    ...mapMutations(["setUser", "setToken"]),
    async loginUser(){
      if(!this.email || !this.password){
        this.error = "Please enter all required fields"
      }
      else {
        let response = await fetch('http://localhost:5000/login?include_auth_token', {
          method: 'POST',
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({email: this.email, password: this.password})
        })
        if (response.status !== 200) {
          console.log('Denied')
          this.error = "Check your credentials please!"
        } else if (response.status === 200) {
          const data = await response.json()
          console.log(data);
          this.setToken(data['response']['user']['authentication_token'])
          await fetch('http://localhost:5000/api/user', {
        method:"GET",
        headers:{
          "Content-Type":"application/json",
          "Authentication-Token":this.$store.state.token
        }
      })
          .then(resp => resp.json())
          .then(user => {this.setUser(user)})
          .catch(error => console.log(error));

        await this.$router.push({
          name:"profile"
        })
        }
      }
      }
    }
}
</script>

<style scoped>
.card-group{
  margin: 41%;
}
</style>