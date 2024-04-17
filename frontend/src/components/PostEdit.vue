<template>
<div class="container mt-4">
  <form @submit.prevent="updatePost">
    <input
    type="text"
    class="form-control"
    placeholder="Please enter your title"
    v-model="title"/>
    <br/>
  <textarea
        rows="10"
        class="form-control"
        placeholder="Please enter your body"
        v-model="body">
    </textarea>
    <br/>
    <input
        type="file"
        accept="image/*"
        class="form-control"
        @change="uploadImage"
    />
    <div id="preview">
    <img v-if="image.imageUrl"
         :src="image.imageUrl"
         :alt="'Preview New Image'"/>
  </div>
    <button
    class="btn btn-success mt-4">
      Save article
    </button>
  </form>
  <div v-if="error" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
    <strong>{{error}}</strong>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      title: null,
      body: null,
      image:{
        image:null,
        imageUrl:null
      },
      error: null
    }
  },
  props:{
    id:{
      type:[Number, String],
      required:true
    }
  },
  methods:{
    updatePost(){
    if(!this.title||!this.body){
        this.error = "Please add all fields"
      }
    else {
      let formData = new FormData
      formData.append('title', this.title);
      formData.append('body', this.body);
      if(this.image.image){
        formData.append('image', this.image.image, this.image.image.name);
      }
      fetch(`http://localhost:5000/api/userposts/${this.id}`, {
        method: "PUT",
        headers: {
          "Authentication-Token": this.$store.state.token
        },
        body: formData
      })
          .then(resp => resp.json())
          .then(() => {
            this.$router.push({
              name: "profile"
            })
          })
          .catch(error => console.log(error))
      }
    },
    uploadImage(e){
      const file = e.target.files[0]
      this.image.image = file
      this.image.imageUrl = URL.createObjectURL(file)
      console.log(file)
    },
    setFields(){
      fetch(`http://localhost:5000/api/userposts/${this.id}`, {
        method: "GET",
        headers :{
          "Authentication-Token": this.$store.state.token
        }
      })
          .then(resp => resp.json())
          .then(data =>{
            this.title = data.title;
            this.body = data.body;
          })
          .catch(err => console.log(err));
    }
  },
  created() {
    if (!(this.user)){
        this.$store.state.user = JSON.parse(localStorage['user'])
        this.$store.state.token = localStorage['token']
        this.user = this.$store.state.user
      }
    this.setFields()
  }
}
</script>

<style scoped>

</style>