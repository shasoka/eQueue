/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
	
    id("kotlin-kapt")
    id("kotlin-parcelize")
	
    id("com.google.dagger.hilt.android")
}

android {
    namespace = "ru.shasoka.equeue"
    compileSdk = 34

    defaultConfig {
        applicationId = "ru.shasoka.equeue"
        minSdk = 26
        //noinspection OldTargetApi
        targetSdk = 33
        versionCode = 1
        versionName = "1.0"
		
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary = true
        }
    }
	
    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro",
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        compose = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.1"
    }
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
	
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.ui.tooling.preview)
    implementation(libs.androidx.material3)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation(libs.androidx.ui.test.junit4)
    debugImplementation(libs.androidx.ui.tooling)
    debugImplementation(libs.androidx.ui.test.manifest)
	
    // Splash Api
    implementation(libs.androidx.core.splashscreen)
	
    // Datastore
    implementation(libs.androidx.datastore.preferences)
	
    // Dagger Hilt for dependency injection
    implementation(libs.hilt.android)
    implementation(libs.androidx.hilt.navigation.compose)
    kapt(libs.hilt.compiler)
	
    // Compose Foundation
    implementation(libs.androidx.foundation)
	
    // Compose Navigation
    implementation(libs.androidx.navigation.compose)
	
    // Retrofit
    implementation(libs.retrofit)
    implementation(libs.converter.gson)
	
    // Room
    implementation(libs.androidx.room.runtime)
    //noinspection KaptUsageInsteadOfKsp
    kapt(libs.androidx.room.compiler)
    implementation(libs.androidx.room.ktx)
}

kapt {
    correctErrorTypes = true
}
