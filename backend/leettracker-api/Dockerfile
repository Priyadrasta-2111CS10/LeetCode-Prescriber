# --- Build stage -----------------------------------------------------
FROM maven:3.9-eclipse-temurin-21 AS build

WORKDIR /app

# Copy just the POM first so dependency downloads are cached across
# rebuilds when only source files change.
COPY pom.xml .
RUN mvn dependency:go-offline -B

COPY src ./src
RUN mvn clean package -DskipTests -B

# --- Run stage ---------------------------------------------------------
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Adjust the jar name/pattern below if your artifactId/version in pom.xml
# produce a different filename than "*.jar" in target/.
COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
