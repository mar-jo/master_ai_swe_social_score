# Use the official .NET 8 runtime image as the base image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 8080

# Use the official .NET 8 SDK image to build the app
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["SocialScoresFrontend/SocialScoresFrontend.csproj", "SocialScoresFrontend/"]
RUN dotnet restore "SocialScoresFrontend/SocialScoresFrontend.csproj"
COPY . .
WORKDIR "/src/SocialScoresFrontend"
RUN dotnet publish "SocialScoresFrontend.csproj" -c Release -o /app/publish

# Final stage: copy the published files and define the entry point
FROM base AS final
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "SocialScoresFrontend.dll"]