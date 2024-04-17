<template>
<div>
  <br>
  <h2>Edit your profile</h2>
  <p><strong>(* marked fields are important)</strong></p>
  <div class="container card-group mt-4">
    <form @submit.prevent="updateProfile">
      <p style="text-align: left">*Username:</p>
      <input
        type="text"
        class="form-control"
        placeholder="Please enter your username"
        v-model="username"
      readonly>
      <br/>
      <p style="text-align: left">*Email Address:</p>
      <input
        type="text"
        class="form-control"
        size="28"
        placeholder="Please enter your email address"
        v-model="email"
      readonly>
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
        type="number"
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
      <button
        class="btn btn-success mt-4">
          Submit
      </button>
      <div v-if="error" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
    <strong>{{error}}</strong>
  </div>
    </form>
  </div>
</div>

</template>

<script>
export default {
  data(){
    return{
      user:this.$store.state.user,
      username:null,
      email:null,
      name:null,
      phone:null,
      bio:null,
      error:null
    }
  },
  methods:{
    setFields(){
      this.username = this.user.username;
      this.email = this.user.email;
      this.name = this.user.name;
      this.phone = this.user.phone;
      this.bio = this.user.bio;
    },

    updateProfile(){
      fetch ('http://localhost:5000/api/user', {
        method:"PUT",
        headers:{
          "Content-Type":"application/json",
          "Authentication-Token":this.$store.state.token
        },
          body:JSON.stringify({
            username:this.username,
            email:this.email,
            name:this.name,
            phone:this.phone,
            bio:this.bio
          })
      })
          .then(resp => resp.json())
          .then(data => {
            this.$store.state.user = data;
            console.log(data);
            this.$router.push({
              name:"profile"
            })
          })
          .catch(err => console.log(err))
    },
  },
  created() {
    if (!(this.user)){
        this.$store.state.user = JSON.parse(localStorage['user'])
        this.$store.state.token = localStorage['token']
        this.user = this.$store.state.user
      }
    this.setFields()
  },
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