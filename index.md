# index.md
---
layout: default
title: "Default Credentials Database"
description: "The ultimate repository for discovering default credentials across various platforms"
---

<div class="hero">
  <h1 class="hero-title">🔐 Credflix</h1>
  <p class="hero-subtitle">
    The ultimate repository for discovering default credentials across various platforms. 
    Simplify your security assessments with our curated lists and enhance your penetration testing efforts.
  </p>
</div>

<div class="container">
  {% include search-bar.html %}
  
  <div class="category-stats">
    <div class="stat-item">
      <span class="stat-number stat-total">{{ site.data.IT_Infrastructures.items.size | plus: site.data.Networking_Equipements.items.size | plus: site.data.IoT.items.size | plus: site.data.Security_Devices.items.size | plus: site.data.Software_Applications.items.size | plus: site.data.Telecommunications_VoIP.items.size }}</span>
      <span class="stat-label">Total Credentials</span>
    </div>
  </div>

  <!-- All credentials combined -->
  {% assign all_items = '' | split: '' %}
  {% for item in site.data.IT_Infrastructures.items %}
    {% assign all_items = all_items | push: item | assign: 'category', 'IT_Infrastructures' %}
  {% endfor %}
  {% for item in site.data.Networking_Equipements.items %}
    {% assign all_items = all_items | push: item | assign: 'category', 'Networking_Equipements' %}
  {% endfor %}
  {% for item in site.data.IoT.items %}
    {% assign all_items = all_items | push: item | assign: 'category', 'IoT' %}
  {% endfor %}
  {% for item in site.data.Security_Devices.items %}
    {% assign all_items = all_items | push: item | assign: 'category', 'Security_Devices' %}
  {% endfor %}
  {% for item in site.data.Software_Applications.items %}
    {% assign all_items = all_items | push: item | assign: 'category', 'Software_Applications' %}
  {% endfor %}
  {% for item in site.data.Telecommunications_VoIP.items %}
    {% assign all_items = all_items | push: item | assign: 'category', 'Telecommunications_VoIP' %}
  {% endfor %}

  <div class="credentials-grid">
    {% for item in site.data.IT_Infrastructures.items %}
      <div class="credential-card" data-category="IT_Infrastructures">
        <div class="card-header">
          <div class="card-title-section">
            <h3 class="card-title">{{ item.name }}</h3>
            <span class="card-vendor">{{ item.vendor }}</span>
            <span class="card-type">{{ item.type }}</span>
          </div>
          <div class="card-actions">
            <button class="btn-copy-all" data-credentials="{{ item.default_credentials | jsonify | escape }}" title="Copy all credentials">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
            </button>
          </div>
        </div>
        
        <p class="card-description">{{ item.description }}</p>
        
        <div class="credentials-table-container">
          <table class="credentials-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Password</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {% for cred in item.default_credentials %}
              <tr>
                <td class="username-cell">
                  <code>{{ cred.username }}</code>
                </td>
                <td class="password-cell">
                  <code>{{ cred.password | default: '(empty)' }}</code>
                </td>
                <td class="action-cell">
                  
