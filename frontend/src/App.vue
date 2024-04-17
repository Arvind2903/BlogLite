<template>
<div id="app">
  <NavBar></NavBar>
  <router-view to="/home"></router-view>
</div>
</template>

<script>
import NavBar from './components/NavComp.vue'

export default {
  id:"app",
  name: 'app',
  components: {
    NavBar
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
