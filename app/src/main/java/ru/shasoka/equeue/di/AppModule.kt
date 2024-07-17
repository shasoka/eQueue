/*
 Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.di

import android.app.Application
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import ru.shasoka.equeue.data.manager.LocalUserManagerImpl
import ru.shasoka.equeue.data.remote.API
import ru.shasoka.equeue.data.repository.APIRepositoryImpl
import ru.shasoka.equeue.domain.manager.LocalUserManager
import ru.shasoka.equeue.domain.repository.APIRepository
import ru.shasoka.equeue.domain.usecases.api.APIUseCases
import ru.shasoka.equeue.domain.usecases.api.LoginUser
import ru.shasoka.equeue.domain.usecases.appentry.AppEntryUseCases
import ru.shasoka.equeue.domain.usecases.appentry.ReadAppEntry
import ru.shasoka.equeue.domain.usecases.appentry.SaveAppEntry
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    @Provides
    @Singleton
    fun provideLocalUserManager(application: Application): LocalUserManager =
        LocalUserManagerImpl(
            application,
        )

    @Provides
    @Singleton
    fun provideAppEntryUseCases(localUserManager: LocalUserManager): AppEntryUseCases =
        AppEntryUseCases(
            readAppEntry = ReadAppEntry(localUserManager),
            saveAppEntry = SaveAppEntry(localUserManager),
        )

    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit =
        Retrofit
            .Builder()
            .baseUrl("https://equeue-backend.onrender.com/api/v1/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()

    @Provides
    @Singleton
    fun provideApi(retrofit: Retrofit): API = retrofit.create(API::class.java)

    @Provides
    @Singleton
    fun provideAPIRepository(api: API): APIRepository = APIRepositoryImpl(api)

    @Provides
    @Singleton
    fun provideAPIUseCases(repository: APIRepository): APIUseCases =
        APIUseCases(
            loginUser = LoginUser(repository),
		)
}
