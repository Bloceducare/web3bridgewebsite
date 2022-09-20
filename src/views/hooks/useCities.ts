import axios from "axios";
import { useState, useEffect, useCallback } from "react";
import { LOCATION_BASE_URL } from "config/constant";

export const useCities = (country) => {
    const [cities, setCities] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const getCities = async (country) => {
        setLoading(true);
        try {
          const {data} = await axios.post(`${LOCATION_BASE_URL}countries/cities`, {
            country: country?.toLowerCase(),
        });
        const dataToSet = data.data.map((city) =>({value: city, label: city}));
            setCities(dataToSet ?? []);
        
        } catch (e:any) {
            setError(e);
        } finally {
            setLoading(false);
        }
    };
    const callabckData = useCallback((country)=>getCities(country), []);
    useEffect(() => {
        if(!country) return;
        callabckData(country)
       
    }, [callabckData, country]);

    return { cities, loading, error };
}

export default useCities