/*
 * Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
 */

package ru.shasoka.equeue.di

import android.app.Application
import androidx.room.Room
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import ru.shasoka.equeue.data.local.EQueueDatabase
import ru.shasoka.equeue.data.local.UserDao
import ru.shasoka.equeue.data.manager.LocalUserManagerImpl
import ru.shasoka.equeue.data.remote.Api
import ru.shasoka.equeue.data.repository.ApiRepositoryImpl
import ru.shasoka.equeue.domain.manager.LocalUserManager
import ru.shasoka.equeue.domain.repository.ApiRepository
import ru.shasoka.equeue.domain.usecases.api.groupselection.GetGroups
import ru.shasoka.equeue.domain.usecases.api.groupselection.GroupSelectionUseCases
import ru.shasoka.equeue.domain.usecases.api.groupselection.JoinGroup
import ru.shasoka.equeue.domain.usecases.api.login.LoginUseCases
import ru.shasoka.equeue.domain.usecases.api.login.LoginUser
import ru.shasoka.equeue.domain.usecases.api.logout.LogoutUseCases
import ru.shasoka.equeue.domain.usecases.api.logout.LogoutUser
import ru.shasoka.equeue.domain.usecases.appentry.AppEntryUseCases
import ru.shasoka.equeue.domain.usecases.appentry.ReadAppEntry
import ru.shasoka.equeue.domain.usecases.appentry.SaveAppEntry
import ru.shasoka.equeue.util.Constants.DB_NAME
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
            .baseUrl("https://equeue.onrender.com/api/v1/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()

    @Provides
    @Singleton
    fun provideApi(retrofit: Retrofit): Api = retrofit.create(Api::class.java)

    @Provides
    @Singleton
    fun provideApiRepository(api: Api): ApiRepository = ApiRepositoryImpl(api)

    @Provides
    @Singleton
    fun provideLoginUseCases(
        repository: ApiRepository,
        userDao: UserDao,
    ): LoginUseCases =
        LoginUseCases(
            loginUser = LoginUser(repository, userDao),
        )

    @Provides
    @Singleton
    fun provideGroupSelectionUseCases(
        repository: ApiRepository,
        userDao: UserDao,
    ): GroupSelectionUseCases =
        GroupSelectionUseCases(
            getGroups = GetGroups(repository, userDao),
            joinGroup = JoinGroup(repository, userDao),
        )

    @Provides
    @Singleton
    fun provideLogoutUserUseCases(userDao: UserDao): LogoutUseCases = LogoutUseCases(logoutUser = LogoutUser(userDao = userDao))

    @Provides
    @Singleton
    fun provideEQueueDatabase(application: Application): EQueueDatabase =
        Room
            .databaseBuilder(
                context = application,
                klass = EQueueDatabase::class.java,
                name = DB_NAME,
            ).fallbackToDestructiveMigration()
            .build()

    @Provides
    @Singleton
    fun provideUserDao(eQueueDatabase: EQueueDatabase): UserDao = eQueueDatabase.userDao
}
