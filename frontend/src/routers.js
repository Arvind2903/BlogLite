import HomeComp from './components/HomeComp'
import CreateComp from './components/CreateComp'
import VueRouter from 'vue-router'
import Vue from "vue";
import LoginComp from "@/components/LoginComp";
import SignupComp from "@/components/SignupComp";
import UserProfileComp from "@/components/UserProfileComp";
import PostDetails from "@/components/PostDetails";
import PostEdit from "@/components/PostEdit";
import ProfileComp from "@/components/ProfileComp";
import UserProfileEdit from "@/components/UserProfileEdit";
import FollowersComp from "@/components/FollowersComp";
import FollowingComp from "@/components/FollowingComp";
import ActivityComp from "@/components/ActivityComp";
Vue.use(VueRouter)
const routes = [
    {
        path:'/',
        name:'login',
        component:LoginComp,
        meta:{
            hideNavbar: true
        }
    },
    {
        path:'/signup',
        name:'signup',
        component:SignupComp,
        meta:{
            hideNavbar: true
        }
    },
    {
        path:'/home',
        name:'home',
        component:HomeComp
    },
    {
        path:'/create',
        name:'create',
        component:CreateComp
    },
    {
        path:'/post/:id',
        name:'postDetails',
        component:PostDetails,
        props:true
    },
    {
        path:'/edit/:id',
        name:'edit',
        component:PostEdit,
        props:true
    },
    {
        path:'/profile',
        name:'profile',
        component:UserProfileComp
    },
    {
        path:'/profile/:id',
        name:'profileDetails',
        component:ProfileComp,
        props:true
    },
    {
        path:'/edit',
        name:'profileEdit',
        component:UserProfileEdit
    },
    {
        path:'/followers',
        name:'followers',
        component: FollowersComp
    },
    {
        path:'/followings',
        name:'followings',
        component: FollowingComp
    },
    {
        path:'/activity',
        name:'activity',
        component: ActivityComp
    }
]

const router = new VueRouter({
    routes
})

export default router