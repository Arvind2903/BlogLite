<template>
<div>
  <br>
  <h2>Sign up to use BlogLite</h2>
  <p><strong>(* marked fields are important)</strong></p>
  <div class="container card-group mt-4">
    <form @submit.prevent="signUp">
      <p style="text-align: left">*Username:</p>
      <input
        type="text"
        class="form-control"
        placeholder="Please choose a username"
        v-model="username">
      <br/>
      <p style="text-align: left">*Email Address: (cannot be changed later)</p>
      <input
        type="text"
        class="form-control"
        size="28"
        placeholder="Please enter your email address"
        v-model="email">
      <br/>
      <p style="text-align: left">*Full Name:</p>
      <input
        type="text"
        class="form-control"
        placeholder="Please enter your full name"
        v-model="name">
      <br/>
      <p style="text-align: left">Phone Number:</p>
      <input
        type="text"
        class="form-control"
        placeholder="Please enter your phone number"
        v-model="phone">
      <br/>
      <p style="text-align: left">Bio:</p>
      <input
        type="text"
        class="form-control"
        placeholder="Please enter your bio"
        v-model="bio">
      <br/>
      <p style="text-align: left">*Password:</p>
      <input
        type="password"
        class="form-control"
        placeholder="Please enter your password"
        v-model="password">
      <br/>
      <p style="text-align: left">*Confirm Password:</p>
      <input
        type="password"
        class="form-control"
        placeholder="Please confirm your password"
        v-model="confirm_password">
      <br/>
      <button
        class="btn"
        style="background-image: url(https://cdn-icons-png.flaticon.com/512/9633/9633868.png);
               background-size: 100%; width: 75px; height: 75px">
      </button>
      <p>Sign Up</p>
      <div v-if="error" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
    <strong>{{error}}</strong>
  </div>
  <div v-if="password_error" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
    <strong>{{password_error}}</strong>
  </div>
    </form>
  </div>
</div>
</template>

<script>
export default {
  data(){
    return{
      username:null,
      email:null,
      name:null,
      phone:null,
      bio:null,
      password:null,
      confirm_password:null,
      error:null,
      password_error:null
    }
  },
  methods:{
    signUp(){
      if(!this.username || !this.email || !this.name || !this.password){
        this.error = "Please add all required fields"
      }
      else if (this.password !== this.confirm_password){
          this.password_error = "Passwords don't match!!!"
      }
      else
        {
          fetch('http://localhost:5000/api/signup',{
          method:'POST',
          headers:{
          "Content-Type":"application/json"
        },
          body:JSON.stringify({username:this.username, email:this.email, name:this.name,
          phone:this.phone, bio:this.bio, password:this.password})
        })
              .then((response) => {
                if (response.ok){
                  this.$router.push({
                    name:"login"
                  })
                  console.log("Signed Up")
                }
                else if(response.status===405){
                  this.error = response.statusText;
                }
                else{
                  this.error = response.statusText;
                }
              })
              .catch(error => console.log(error))
        }
      }
    }
}
</script>

<style scoped>
.card-group{
  margin: 41%;
}
input::placeholder{
  text-align: center;
}
</style>