import Vue from 'vue';
import Router from 'vue-router';

import Layout from '@/components/Layout/Layout';

// Pages
import Login from "@/pages/Login/Login";
import Dashboard from '@/pages/Dashboard/Dashboard';
import Conferences from '@/pages/Conferences/Conferences'
import Amphitheatres from '@/pages/Amphitheatres/Amphitheatres'
import DetailsAmphitheatre from '@/pages/Amphitheatres/DetailsAmphitheatre'
import Participants from '@/pages/Participants/Participants'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
    path: '/',
    redirect: 'login',
    name: 'Layout',
    component: Layout,
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard,
      },
      {
        path: 'conferences',
        name: 'Conferences',
        component: Conferences,
      },
      {
        path: 'amphitheatres',
        name: 'Amphitheatres',
        component: Amphitheatres
      },
      {
        path: 'amphitheatres/details/:id',
        name: 'DetailsAmphitheatre',
        component: DetailsAmphitheatre
      },
      {
        path: 'participants',
        name: 'Participants',
        component: Participants
      },
     
    ],
  },
    {
      path: '*',
      name: 'Error',
      component: Error
    }
  ],
});
