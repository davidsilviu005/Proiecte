package org.example;

public class Location {
    private final String country;
    private final String city;
    private final String address;
    private final Double latitude;
    private final Double longitude;

    public Location(String country, String city, String address, Double latitude, Double longitude) {
        this.country = country;
        this.city = city;
        this.address = address;
        this.latitude = latitude;
        this.longitude = longitude;
    }

    public String getCity() {
        return city;
    }

    public String getAddress() {
        return address;
    }

    public Double getLongitude() {
        return longitude;
    }

    public Double getLatitude() {
        return latitude;
    }

    public String getCountry() {
        return country;
    }
}
