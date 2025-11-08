import { priceFormattersType } from "@/types/api/prices";

const formatPrice = (price: number, formatter: priceFormattersType): string => {
    switch (formatter) {
        case 'equal':
            return price.toString();
        case 'gt':
            return `от ${price.toString()}`;
        case 'lt':
            return `до ${price.toString()}`;
        case 'discuss':
            return 'договорная';
    }
}

export default formatPrice;